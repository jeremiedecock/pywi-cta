#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

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

import math

import numpy as np

from pywicta.image.hillas_parameters import get_hillas_parameters
from pywicta.io import geometry_converter

class Criteria:

    def __init__(self, cam_id, min_npe, max_npe, min_radius, max_radius, min_ellipticity, max_ellipticity):
        self.cam_id = cam_id
        self.geom1d = geometry_converter.get_geom1d(self.cam_id)
        self.hillas_implementation = 2

        self.min_npe = min_npe
        self.max_npe = max_npe
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_ellipticity = min_ellipticity
        self.max_ellipticity = max_ellipticity

    def hillas_parameters(self, image):
        hillas_params = get_hillas_parameters(self.geom1d, image, self.hillas_implementation)
        return hillas_params

    def hillas_ellipticity(self, image, hillas_params):
        length = hillas_params.length.value
        width = hillas_params.width.value

        if length == 0:
            ellipticity = 0
        else:
            ellipticity = width / length

        return ellipticity

    def hillas_centroid_dist(self, image, hillas_params):
        x = hillas_params.cen_x.value
        y = hillas_params.cen_y.value

        return math.sqrt(x**2 + y**2)

    def __call__(self, images2d):
        ref_image_2d = images2d.reference_image
        ref_image_1d = geometry_converter.image_2d_to_1d(ref_image_2d, self.cam_id)
        hillas_params = self.hillas_parameters(ref_image_1d)

        npe_contained = self.min_npe < np.nansum(ref_image_1d) < self.max_npe
        ellipticity_contained = self.min_ellipticity < self.hillas_ellipticity(ref_image_1d, hillas_params) < self.max_ellipticity
        radius_contained = self.min_radius < self.hillas_centroid_dist(ref_image_1d, hillas_params) < self.max_radius

        return not (npe_contained and ellipticity_contained and radius_contained)