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

import numpy as np

from pywicta.benchmark import assess
from pywicta.io import geometry_converter

###############################################################################

def test_all_zeros():
    """Test all metrics with an input, output and reference image full of zeros."""
    cam_id = "LSTCam"
    geom1d = geometry_converter.get_geom1d(cam_id)

    shape = geom1d.pix_x.shape
    dtype = "float"

    inp_img = np.zeros(shape=shape, dtype=dtype)
    out_img = np.zeros(shape=shape, dtype=dtype)
    ref_img = np.zeros(shape=shape, dtype=dtype)

    inp_img_2d = geometry_converter.image_1d_to_2d(inp_img, cam_id)
    out_img_2d = geometry_converter.image_1d_to_2d(out_img, cam_id)
    ref_img_2d = geometry_converter.image_1d_to_2d(ref_img, cam_id)

    score_tuple, metrics_name_tuple = assess.assess_image_cleaning(inp_img_2d,
                                                                   out_img_2d,
                                                                   ref_img_2d,
                                                                   benchmark_method="all",
                                                                   geom=geom1d)

    assert len(score_tuple) == len(metrics_name_tuple)
    assert len(score_tuple) > 1


def test_metric_roc():

    ref = np.array([[0, 1, 0],
                    [2, 3, 2],
                    [0, 1, 0]])
    
    out = np.array([[0., 3., 0.],
                    [2., 0., 3.],
                    [1., 1., 2.]])
    
    res = assess.metric_roc(None, out, ref)
    
    assert res.roc_true_positives == 4 \
           and res.roc_false_positives == 2 \
           and res.roc_true_negatives == 2 \
           and res.roc_false_negatives == 1


def test_metric_roc_with_nan_values():

    ref = np.array([[0, 1, 0],
                    [2, 3, 2],
                    [0, 1, np.nan]])
    
    out = np.array([[0., 3., np.nan],
                    [2., 0., np.nan],
                    [1., 1., np.nan]])
    
    res = assess.metric_roc(None, out, ref)
    
    # NaN is count as True
    assert res.roc_true_positives == 5 \
           and res.roc_false_positives == 2 \
           and res.roc_true_negatives == 1 \
           and res.roc_false_negatives == 1

