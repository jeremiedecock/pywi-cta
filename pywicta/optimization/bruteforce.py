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

__all__ = []

import json
from scipy import optimize
#from pywicta.optimization.objectivefunc.wavelets_mrfilter_delta_psi import ObjectiveFunction as WaveletMRFObjectiveFunction
from pywicta.optimization.objectivefunc.wavelets_mrfilter_all import ObjectiveFunction as WaveletMRFObjectiveFunction
#from pywicta.optimization.objectivefunc.wavelets_mrtransform_delta_psi import ObjectiveFunction as WaveletMRTObjectiveFunction
from pywicta.optimization.objectivefunc.wavelets_mrtransform_all import ObjectiveFunction as WaveletMRTObjectiveFunction
#from pywicta.optimization.objectivefunc.tailcut_delta_psi import ObjectiveFunction as TailcutObjectiveFunction
from pywicta.optimization.objectivefunc.tailcut_all import ObjectiveFunction as TailcutObjectiveFunction

# For wavelets
import pywicta.denoising.cdf
from pywicta.denoising.inverse_transform_sampling import EmpiricalDistribution

def main():

    #algo = "wavelet_mrfilter"
    algo = "wavelet_mrtransform"
    #algo = "tailcut"

    #instrument = "ASTRICam"
    #instrument = "CHEC"
    #instrument = "DigiCam"
    #instrument = "FlashCam"
    #instrument = "NectarCam"
    instrument = "LSTCam"

    #max_num_img = None
    max_num_img = 1000

    aggregation_method = "mean"
    #aggregation_method = "median"

    kill_islands = False

    cleaning_failure_score = 90.
    #cleaning_failure_score = float('nan')

    faint = True

    num_scales = 3

    print("algo:", algo)
    print("instrument:", instrument)
    print("kill_islands:", kill_islands)

    if instrument == "ASTRICam":

        input_files = ["/dev/shm/.jd/astri/gamma/"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.ASTRI_CDF_FILE)

        if algo == "wavelet_mrfilter":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "wavelet_mrtransform":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "tailcut":
            search_ranges = (slice(-2., 10., 0.5),     # Core threshold (largest threshold)
                             slice(-2., 10., 0.5))     # Boundary threshold (smallest threshold)

    elif instrument == "CHEC":

        input_files = ["/dev/shm/.jd/gct/gamma/"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.GCT_CDF_FILE)

        if algo == "wavelet_mrfilter":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "wavelet_mrtransform":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "tailcut":
            search_ranges = (slice(-2., 10., 0.5),     # Core threshold (largest threshold)
                             slice(-2., 10., 0.5))     # Boundary threshold (smallest threshold)

    elif instrument == "DigiCam":

        input_files = ["/dev/shm/.jd/digicam/gamma/"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.DIGICAM_CDF_FILE)

        if algo == "wavelet_mrfilter":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "wavelet_mrtransform":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "tailcut":
            search_ranges = (slice(-2., 10., 0.5),     # Core threshold (largest threshold)
                             slice(-2., 10., 0.5))     # Boundary threshold (smallest threshold)

    elif instrument == "FlashCam":

        input_files = ["/dev/shm/.jd/flashcam/gamma/"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.FLASHCAM_CDF_FILE)

        if algo == "wavelet_mrfilter":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "wavelet_mrtransform":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "tailcut":
            search_ranges = (slice(-2., 10., 0.5),     # Core threshold (largest threshold)
                             slice(-2., 10., 0.5))     # Boundary threshold (smallest threshold)

    elif instrument == "NectarCam":

        input_files = ["/dev/shm/.jd/nectarcam/gamma/"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.NECTARCAM_CDF_FILE)

        if algo == "wavelet_mrfilter":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "wavelet_mrtransform":
            search_ranges = (slice(1, 5, 1),           # Scale 0 (smallest scale)
                             slice(1, 5, 1),           # Scale 1
                             slice(1, 5, 1),           # Scale 2
                             slice(1, 5, 1))           # Scale 3 (largest scale)
        elif algo == "tailcut":
            search_ranges = (slice(-2., 10., 0.5),     # Core threshold (largest threshold)
                             slice(-2., 10., 0.5))     # Boundary threshold (smallest threshold)

    elif instrument == "LSTCam":

        if faint:
            input_files = ["/dev/shm/.jd/lstcam/gamma/lst_faint/"]
        else:
            input_files = ["/dev/shm/.jd/lstcam/gamma/"]

        #input_files = ["~/data/grid_prod3b_north/simtel/gamma"]
        noise_distribution = EmpiricalDistribution(pywicta.denoising.cdf.LSTCAM_CDF_FILE)

        if algo == "wavelet_mrfilter":

            search_ranges = (slice(1., 14., 1.),      # Scale 0 (smallest scale)
                             slice(1., 9.,  1.),      # Scale 1
                             slice(1., 6.,  1.))      # Scale 3 (largest scale aside residuals)

        elif algo == "wavelet_mrtransform":

            if num_scales == 3:

                search_ranges = (slice(0., 15., 1.),      # Scale 0 (smallest scale)
                                 slice(0., 2.,  0.2))     # Scale 1 (larger scale)

            elif num_scales == 4:

                search_ranges = (slice(0., 15., 1.),      # Scale 0 (smallest scale)
                                 slice(0., 2.,  0.2),     # Scale 1 (larger scale)
                                 slice(0., 0.75, 0.05))  # Scale 2

            elif num_scales == 5:

                search_ranges = (slice(0., 15., 1.),      # Scale 0 (smallest scale)
                                 slice(0., 2.,  0.2),     # Scale 1 (larger scale)
                                 slice(0., 0.75, 0.05),  # Scale 2
                                 slice(0., 0.3, 0.05))   # Scale 3

        elif algo == "tailcut":

            search_ranges = (slice(1., 10., 0.5),     # Core threshold (largest threshold)
                             slice(1., 10., 0.5))     # Boundary threshold (smallest threshold)

    else:

        raise Exception("Unknown instrument", instrument)

    print("input_files:", input_files)
    print("noise_distribution:", noise_distribution.cdf_json_file_path)

    if algo == "wavelet_mrfilter":

        func = WaveletMRFObjectiveFunction(input_files=input_files,
                                           cam_id=instrument,
                                           noise_distribution=noise_distribution,
                                           max_num_img=max_num_img,
                                           aggregation_method=aggregation_method,  # "mean" or "median"
                                           kill_isolated_pixels=kill_islands,
                                           cleaning_failure_score=cleaning_failure_score)

    elif algo == "wavelet_mrtransform":

        func = WaveletMRTObjectiveFunction(input_files=input_files,
                                           cam_id=instrument,
                                           noise_distribution=noise_distribution,
                                           max_num_img=max_num_img,
                                           aggregation_method=aggregation_method,  # "mean" or "median"
                                           kill_isolated_pixels=kill_islands,
                                           cleaning_failure_score=cleaning_failure_score)

    elif algo == "tailcut":

        func = TailcutObjectiveFunction(input_files=input_files,
                                        cam_id=instrument,
                                        max_num_img=max_num_img,
                                        aggregation_method=aggregation_method,  # "mean" or "median"
                                        kill_isolated_pixels=kill_islands,
                                        cleaning_failure_score=cleaning_failure_score)

    else:

        raise ValueError("Unknown algorithm", algo)

    res = optimize.brute(func,
                         search_ranges,
                         full_output=True,
                         finish=None)     #optimize.fmin)

    print("x* =", res[0])
    print("f(x*) =", res[1])

    # SAVE RESULTS ############################################################

    res_dict = {
                "best_solution": res[0].tolist(),
                "best_score": float(res[1]),
                "solutions": res[2].tolist(),
                "scores": res[3].tolist(),
                "others_scores": func.aggregated_score_list if hasattr(func, "aggregated_score_list") else None,
                "instrument": instrument,
                "algo": algo_label,
                "algo_params": func.algo_params if hasattr(func, "algo_params") else None,
                "max_num_img": max_num_img,
                "npe_range": "faint" if faint else "faint-and-bright",
                "aggregation_method": aggregation_method,
                "remove_islands": "kill" if kill_islands else "nokill",
                "cleaning_failure_score": str(cleaning_failure_score)
               }

    if algo in ("wavelet_mrtransform", "wavelet_mrfilter"):
        algo_label = "{}_{}scales".format(algo, num_scales)
    else:
        algo_label = algo

    file_base_name = "optimize_{}_{}_{}_{}_{}_{}_{}".format(instrument,
                                                            algo_label,
                                                            max_num_img,
                                                            "faint" if faint else "faint-and-bright",
                                                            aggregation_method,
                                                            "kill" if kill_islands else "nokill",
                                                            str(cleaning_failure_score))
    with open(file_base_name + "_default.json", "w") as fd:
        json.dump(res_dict, fd, sort_keys=True, indent=4)  # pretty print format

    #try:
    #    with open(file_base_name + "_all.json", "w") as fd:
    #        json.dump(func.aggregated_score_list, fd, sort_keys=True, indent=4)  # pretty print format
    #except:
    #    print("All metrics statistics not available")


if __name__ == "__main__":
    main()

