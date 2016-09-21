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

"""
Denoise FITS and PNG images with Wavelet Transform.

This script use mr_filter -- a program written CEA/CosmoStat
(www.cosmostat.org) -- to make Wavelet Transform.

It originally came from
https://github.com/jdhp-sap/snippets/blob/master/mr_filter/mr_filter_wrapper_denoising.py.

Example usages:
  ./denoising_with_wavelets_mr_filter.py -h
  ./denoising_with_wavelets_mr_filter.py ./test.fits
  ipython3 -- ./denoising_with_wavelets_mr_filter.py -n4 ./test.fits

This script requires the mr_filter program
(http://www.cosmostat.org/software/isap/).

It also requires Numpy and Matplotlib Python libraries.
"""

__all__ = ['wavelet_transform']

import argparse
import datetime
import json
import os
import numpy as np
import time

from datapipe.benchmark import assess
from datapipe.io import images


def wavelet_transform(input_img, number_of_scales=4, base_file_path="wavelet", verbose=False):
    """
    Do the wavelet transform.

    mr_filter
    -K         Suppress the last scale (to have background pixels = 0)
    -k         Suppress isolated pixels in the support
    -F2        First scale used for the detection (smooth the resulting image)
    -C1        Coef_Detection_Method: K-SigmaNoise Threshold
    -s3        K-SigmaNoise Threshold = 3 sigma
    -m2        Noise model (try -m2 or -m10) -> -m10 works better but is much slower...

    eventuellement -w pour le debug
    -p  ?      Detect only positive structure
    -P  ?      Suppress the positivity constraint
    """

    input_file_path = base_file_path + "_in.fits"
    mr_output_file_path = base_file_path + "_out.fits"

    # WRITE THE INPUT FILE (FITS) ##########################

    images.save(input_img, input_file_path)

    # EXECUTE MR_FILTER ####################################

    # TODO: improve the following lines
    #cmd = 'mr_filter -K -k -C1 -s3 -m2 -p -P -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)
    cmd = 'mr_filter -K -k -C1 -s3 -m3 -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)
    os.system(cmd)

    # READ THE MR_FILTER OUTPUT FILE #######################

    cleaned_img = images.load(mr_output_file_path, 0)

    if cleaned_img.ndim != 2:
        raise Exception("Unexpected error: the output FITS file should contain a 2D array.")

    return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")

    parser.add_argument("--hdu", "-H", type=int, default=0, metavar="INTEGER", 
                        help="The index of the HDU image to use for FITS input files")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", action="store_true",
                        help="Save images")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    benchmark_method = args.benchmark
    number_of_scales = args.number_of_scales
    hdu_index = args.hdu
    plot = args.plot
    saveplot = args.saveplot
    input_file_or_dir_path_list = args.fileargs

    if benchmark_method is not None:
        file_path_list = []
        score_list = []
        execution_time_list = []

    for input_file_or_dir_path in input_file_or_dir_path_list:

        if os.path.isdir(input_file_or_dir_path):
            input_file_path_list = []
            for dir_item in os.listdir(input_file_or_dir_path):
                dir_item_path = os.path.join(input_file_or_dir_path, dir_item)
                if dir_item_path.lower().endswith('.fits') and os.path.isfile(dir_item_path):
                    input_file_path_list.append(dir_item_path)
        else:
            input_file_path_list = [input_file_or_dir_path]

        for input_file_path in input_file_path_list:

            # READ THE INPUT FILE #################################################

            input_img = images.load(input_file_path, hdu_index)

            if input_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


            # WAVELET TRANSFORM WITH MR_FILTER ####################################

            base_file_path = os.path.basename(input_file_path)
            base_file_path = os.path.splitext(base_file_path)[0]

            initial_time = time.perf_counter()
            cleaned_img = wavelet_transform(input_img, number_of_scales, base_file_path)
            execution_time = time.perf_counter() - initial_time

            # GET THE REFERENCE IMAGE #############################################

            reference_img = images.load(input_file_path, 1)

            # ASSESS OR PRINT THE CLEANED IMAGE ###################################

            if benchmark_method is not None:
                try:
                    score_tuple = assess.assess_image_cleaning(input_img, cleaned_img, reference_img, benchmark_method)

                    file_path_list.append(input_file_path)
                    score_list.append(score_tuple)
                    execution_time_list.append(execution_time)
                except assess.EmptyReferenceImageError:
                    print("Empty reference image error")
                except assess.EmptyOutputImageError:
                    # TODO: if only the output is zero then this is ackward: this
                    #       is an algorithm mistake but it cannot be assessed...
                    print("Empty output image error")

            # PLOT IMAGES #########################################################

            if plot or saveplot:
                image_list = [input_img, reference_img, cleaned_img] 
                title_list = ["Input image", "Reference image", "Cleaned image"] 

                if plot:
                    images.plot_list(image_list, title_list)

                if saveplot:
                    if 'score_tuple' in locals():              # Not very Pythonic...
                        for score_index, score in enumerate(score_tuple):
                            output = "{}_{}_wt_mrfilter_{}_{}.pdf".format(benchmark_method, score_index, score, base_file_path)
                            images.mpl_save_list(image_list, output, title_list)
                    else:
                        output = "{}_wt_mrfilter.pdf".format(base_file_path)
                        images.mpl_save_list(image_list, output, title_list)

    if benchmark_method is not None:
        print(score_list)

        output_dict = {}
        output_dict["algo"] = __file__
        output_dict["label"] = "WT MrFilter"
        output_dict["algo_params"] = {"number_of_scales": number_of_scales}
        output_dict["benchmark_method"] = benchmark_method
        output_dict["date_time"] = str(datetime.datetime.now())
        output_dict["hdu_index"] = hdu_index
        output_dict["system"] = " ".join(os.uname())
        output_dict["input_file_path_list"] = file_path_list
        output_dict["score_list"] = score_list
        output_dict["execution_time_list"] = execution_time_list

        if args.output is None:
            output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
        else:
            output_file_path = args.output

        with open(output_file_path, "w") as fd:
            #json.dump(data, fd)                                 # no pretty print
            json.dump(output_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == "__main__":
    main()
