#!/bin/sh

ROOT_OUTPUT_DIR=.

# LST
rm -rf ${ROOT_OUTPUT_DIR}/lst_faint
rm -rf ${ROOT_OUTPUT_DIR}/lst_bright
mkdir ${ROOT_OUTPUT_DIR}/lst_faint
mkdir ${ROOT_OUTPUT_DIR}/lst_bright
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 50  --max-npe 177  --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.9036 --camid LSTCam --time-slices -o ${ROOT_OUTPUT_DIR}/lst_faint ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 177 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.9036 --camid LSTCam --time-slices -o ${ROOT_OUTPUT_DIR}/lst_bright ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz

# NectarCam
rm -rf ${ROOT_OUTPUT_DIR}/nectarcam_faint
rm -rf ${ROOT_OUTPUT_DIR}/nectarcam_bright
mkdir ${ROOT_OUTPUT_DIR}/nectarcam_faint
mkdir ${ROOT_OUTPUT_DIR}/nectarcam_bright
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 50  --max-npe 232  --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.906 --camid NectarCam --time-slices -o ${ROOT_OUTPUT_DIR}/nectarcam_faint ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 232 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.906 --camid NectarCam --time-slices -o ${ROOT_OUTPUT_DIR}/nectarcam_bright ~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run104___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz

# SST-1M
rm -rf ${ROOT_OUTPUT_DIR}/sst1m_faint
rm -rf ${ROOT_OUTPUT_DIR}/sst1m_bright
mkdir ${ROOT_OUTPUT_DIR}/sst1m_faint
mkdir ${ROOT_OUTPUT_DIR}/sst1m_bright
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 40  --max-npe 120  --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.357 --camid DigiCam --time-slices -o ${ROOT_OUTPUT_DIR}/sst1m_faint ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 120 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.357 --camid DigiCam --time-slices -o ${ROOT_OUTPUT_DIR}/sst1m_bright ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz

# GCT
rm -rf ${ROOT_OUTPUT_DIR}/gct_faint
rm -rf ${ROOT_OUTPUT_DIR}/gct_bright
mkdir ${ROOT_OUTPUT_DIR}/gct_faint
mkdir ${ROOT_OUTPUT_DIR}/gct_bright
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 40  --max-npe 124  --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.125 --camid CHEC --time-slices -o ${ROOT_OUTPUT_DIR}/gct_faint ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 124 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.125 --camid CHEC --time-slices -o ${ROOT_OUTPUT_DIR}/gct_bright ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz

# Astri
rm -rf ${ROOT_OUTPUT_DIR}/astri_faint
rm -rf ${ROOT_OUTPUT_DIR}/astri_bright
mkdir ${ROOT_OUTPUT_DIR}/astri_faint
mkdir ${ROOT_OUTPUT_DIR}/astri_bright
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 50  --max-npe 193  --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.14 --camid ASTRICam --time-slices -o ${ROOT_OUTPUT_DIR}/astri_faint ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz
./pywicta/io/simtel_to_fits.py --max-images 10000 --min-npe 193 --max-npe 2000 --min-ellipticity 0.1 --max-ellipticity 0.6 --max-radius 0.14 --camid ASTRICam --time-slices -o ${ROOT_OUTPUT_DIR}/astri_bright ~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma/gamma_20deg_180deg_run2203___cta-prod3-sst-dc_desert-2150m-Paranal-sst-dc.simtel.gz
