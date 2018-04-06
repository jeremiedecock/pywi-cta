#!/bin/sh
./pywicta/io/simtel_to_fits.py --max-images 20 --min-npe 50 --max-npe 190 --min-ellipticity 0.1 --max-ellipticity 0.6 --camid LSTCam --time-slices -o faint ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 20 --min-npe 190 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --camid LSTCam --time-slices -o bright ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz
