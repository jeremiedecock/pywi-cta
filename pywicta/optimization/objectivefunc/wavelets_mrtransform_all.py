#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ = ['ObjectiveFunction']

import numpy as np

from pywicta.denoising.wavelets_mrtransform import WaveletTransform
from pywicta.benchmark import assess
from pywicta.benchmark.assess import norm_angle_diff

import os
import time
import shutil

# OPTIMIZER ##################################################################

class ObjectiveFunction:

    def __init__(self,
                 input_files,
                 cam_id,
                 noise_distribution=None,
                 max_num_img=None,
                 aggregation_method="mean",
                 kill_isolated_pixels=False,
                 cleaning_failure_score=90.):

        self.call_number = 0

        # Init the wavelet class
        self.cleaning_algorithm = WaveletTransform()

        # Make the image list
        self.input_files = input_files
        self.max_num_img = max_num_img

        self.cam_id = cam_id

        self.noise_distribution = noise_distribution

        self.aggregation_method = aggregation_method  # "mean" or "median"

        self.kill_isolated_pixels = kill_isolated_pixels

        self.cleaning_failure_score = cleaning_failure_score

        print("aggregation method:", self.aggregation_method)

        self.aggregated_score_list = []

        # PRE PROCESSING FILTERING ############################################

        # TODO...


    def __call__(self, filter_thresholds):
        self.call_number += 1

        aggregated_score = []

        if isinstance(filter_thresholds, (np.ndarray, np.generic) ):
            filter_thresholds_list = filter_thresholds.tolist()
        else:
            filter_thresholds_list = filter_thresholds

        try:
            algo_params_var = {
                        "filter_thresholds": filter_thresholds_list
                    }

            benchmark_method = "all"          # TODO

            label = "WT_MRT_{}".format(self.call_number)
            self.cleaning_algorithm.label = label

            #output_file_path = "score_wavelets_mrt_optim_{}.json".format(self.call_number)
            output_file_path = None

            # Make the temp file directory
            tmp_files_directory = "/dev/shm/.jd/{}_{}".format(os.getpid(), time.time())
            if not os.path.exists(tmp_files_directory):
                os.makedirs(tmp_files_directory)

            algo_params = {
                        "type_of_filtering": "hard_filtering",   # hard_filtering, ksigma_hard_filtering, common_hard_filtering
                        #"filter_thresholds": hard_filter.DEFAULT_FILTER_THRESHOLDS,
                        "last_scale_treatment": "drop",          # keep, drop, mask
                        "detect_only_positive_structures": False,
                        "kill_isolated_pixels": self.kill_isolated_pixels,
                        "noise_distribution": self.noise_distribution,
                        "tmp_files_directory": tmp_files_directory
                    }

            algo_params.update(algo_params_var)

            # TODO: randomly make a subset fo self.input_files
            input_files = self.input_files

            #rejection_criteria = lambda image: not 50 < np.nansum(image.reference_image) < 200

            output_dict = self.cleaning_algorithm.run(algo_params,
                                                      input_file_or_dir_path_list=input_files,
                                                      benchmark_method=benchmark_method,
                                                      output_file_path=output_file_path,
                                                      max_num_img=self.max_num_img,
                                                      cam_id=self.cam_id)
                                                      #rejection_criteria=rejection_criteria)

            score_list = []

            # Read and compute results from output_dict
            for image_dict in output_dict["io"]:

                # POST PROCESSING FILTERING #######################################

                # >>>TODO<<<: Filter images: decide wether the image should be used or not ? (contained vs not contained)
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                # >>>TODO<<<: Filter images by energy range: decide wether the image should be used or not ?
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                ###################################################################

                # GET THE CLEANED IMAGE SCORE

                if "score" in image_dict:
                    scores = [score for score in image_dict["score"]]
                else:
                    # The cleaning algorithm failed to clean this image
                    # TODO: add a penalty
                    scores = []

                # WORKAROUND

                if ("img_ref_hillas_2_psi" in image_dict) and ("img_cleaned_hillas_2_psi" in image_dict):
                    output_image_parameter_psi_rad = image_dict["img_ref_hillas_2_psi"]
                    reference_image_parameter_psi_rad = image_dict["img_cleaned_hillas_2_psi"]
                    delta_psi_rad = reference_image_parameter_psi_rad - output_image_parameter_psi_rad
                    normalized_delta_psi_deg = norm_angle_diff(np.degrees(delta_psi_rad))

                    #if image_dict["score_name"][0] != "delta_psi":
                    #    raise Exception("Cannot get the score")
                    #normalized_delta_psi_deg = image_dict["score"][0]

                    scores.append(normalized_delta_psi_deg)
                else:
                    # The cleaning algorithm failed to clean this image
                    # TODO: add a penalty
                    scores.append(self.cleaning_failure_score)  # the worst score

                score_list.append(scores)

            score_array = np.array(score_list)

            # Compute the mean
            if self.aggregation_method == "mean":
                aggregated_score = np.nanmean(score_array, axis=0)
            elif self.aggregation_method == "median":
                aggregated_score = np.nanmedian(score_array, axis=0)
            else:
                raise ValueError("Unknown value for aggregation_method: {}".format(self.aggregation_method))

            # TODO: save results in a JSON file (?)
            print(algo_params_var, aggregated_score, self.aggregation_method)

            # Remove the temp file directory
            shutil.rmtree(tmp_files_directory)
        except Exception as e:
            print(e)

        self.aggregated_score_list.append([float(score) for score in aggregated_score])

        return float(aggregated_score[-1])    # TODO: use name instead of index...


if __name__ == "__main__":
    # Test...

    func = ObjectiveFunction(input_files=["~/data/grid_prod3b_north/fits/lst/gamma/lst_faint/"],
                             max_num_img=10,
                             cam_id="LSTCam")
    #func = ObjectiveFunction(input_files=["./testset/gamma/astri/tel1/"])
    #func = ObjectiveFunction(input_files=["/Volumes/ramdisk/flashcam/fits/gamma/"])

    filter_thresholds_list = [4, 2, 1]

    score = func(filter_thresholds_list)

