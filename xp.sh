#!/bin/sh

. ./utils/init.sh

# SETUP #######################################################################

NUM_IMG=20000
#NUM_IMG=100

# INSTRUMENT ##########################

#INST="astri_mini_konrad"
#INST="gct_mini_konrad"
#INST="digicam_mini_konrad"

#INST="flashcam_grid_prod3b_north"
#INST="nectarcam_grid_prod3b_north"

INST="lstcam_grid_prod3b_north"

###############################################################################
###############################################################################
###############################################################################

echo "NUM_IMG: ${NUM_IMG}"
echo "INST: ${INST}"

# SYSTEM ##############################

if [ -d /Volumes ]
then
    SYS_NAME="macos"
elif [ -d /proc ]
then
    SYS_NAME="linux"
else
    echo "Unknown system"
    exit 1
fi

echo "SYS_NAME: ${SYS_NAME}"

case ${SYS_NAME} in
macos)
    export PYTHONPATH=.:$PYTHONPATH ;
    if [ -d /Volumes/ramdisk ]
    then
        MR_TMP_DIR="/Volumes/ramdisk"
    else
        MR_TMP_DIR="."
        echo "*** WARNING: CANNOT USE RAMDISK FOR TEMPORARY FILES ; USE ./ INSTEAD... ***"
    fi
    ;;
linux)
    export PYTHONPATH=.:~/git/pub/ext/ctapipe-extra:$PYTHONPATH ;
    if [ -d /dev/shm/.jd ]
    then
        MR_TMP_DIR="/dev/shm/.jd"
    else
        MR_TMP_DIR="."
        echo "*** WARNING: CANNOT USE RAMDISK FOR TEMPORARY FILES ; USE ./ INSTEAD... ***"
    fi
    ;;
*)
    echo "Unknown system" ;
    exit 1
    ;;
esac

echo "MR_TMP_DIR: ${MR_TMP_DIR}"

# DENOISING PARAMETERS AND INPUT FILES ########################################

# TODO
#GAMMA_FITS_DIR=${MR_TMP_DIR}/astri_data/fits/gamma
#PROTON_FITS_DIR=${MR_TMP_DIR}/astri_data/fits/proton

# TODO
#GAMMA_FITS_DIR=${MR_TMP_DIR}/astri_data/fits_flashcam/gamma
#PROTON_FITS_DIR=${MR_TMP_DIR}/astri_data/fits_flashcam/proton

case ${INST} in
astri_mini_inaf)
    CAM_ID="ASTRICam"

    GAMMA_FITS_DIR=~/data/astri_mini_array/fits/astri/gamma ;
    PROTON_FITS_DIR=~/data/astri_mini_array/fits/astri/proton ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/astri_konrad_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="7" ; # Tino
    #TC_LTH="5" ; # Tino
    #TC_LABEL="Tailcut-Tino-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="7" ;   # CTA Abelardo 2nd pass
    TC_LTH="3.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2016
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3       --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3"

    ## 2017/02 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s1,1,2,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s1-1-2-1" ;
    ;;
astri_mini_konrad)
    CAM_ID="ASTRICam"

    #GAMMA_FITS_DIR=~/data/astri_mini_array_konrad/fits/astri_v2/gamma ;
    #PROTON_FITS_DIR=~/data/astri_mini_array_konrad/fits/astri_v2/proton ;
    GAMMA_FITS_DIR=~/data/astri_mini_array_konrad/simtel/astri_v2/gamma/ ;
    PROTON_FITS_DIR=~/data/astri_mini_array_konrad/simtel/astri_v2/proton/ ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/astri_konrad_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="7" ; # Tino
    #TC_LTH="5" ; # Tino
    #TC_LABEL="Tailcut-Tino-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="7" ;   # CTA Abelardo 2nd pass
    TC_LTH="3.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2017/02 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,1,3.5,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-1-3.5-1" ;
    ;;
gct_mini_konrad)
    CAM_ID="CHEC"

    #GAMMA_FITS_DIR=~/data/gct_mini_array_konrad/fits/gct/gamma ;
    #PROTON_FITS_DIR=~/data/gct_mini_array_konrad/fits/gct/proton ;
    GAMMA_FITS_DIR=~/data/gct_mini_array_konrad/simtel/gct/gamma/ ;
    PROTON_FITS_DIR=~/data/gct_mini_array_konrad/simtel/gct/proton/ ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/gct_konrad_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ; # CTA Abelardo 1st pass
    #TC_LTH="2" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="2" ; # CTA Abelardo 2nd pass
    TC_LTH="1" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;
    ;;
digicam_mini_konrad)
    CAM_ID="DigiCam"

    #GAMMA_FITS_DIR=~/data/sst1m_mini_array_konrad/fits/sst1m/gamma ;
    #PROTON_FITS_DIR=~/data/sst1m_mini_array_konrad/fits/sst1m/proton ;
    GAMMA_FITS_DIR=~/data/sst1m_mini_array_konrad/simtel/sst1m/gamma ;
    PROTON_FITS_DIR=~/data/sst1m_mini_array_konrad/simtel/sst1m/proton ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/digicam_konrad_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ;  # HESS
    #TC_LTH="5" ;   # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="6" ;   # CTA Abelardo 1st pass
    #TC_LTH="3" ;   # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="3" ;   # CTA Abelardo 2nd pass
    #TC_LTH="1.5" ; # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="4" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LTH="1" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LABEL="Tailcut-BF1-${TC_HTH}-${TC_LTH}" ;

    ## 2017/09/11 (BF res1) (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,3,4,4 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-3-4-4" ;

    # 2017/10/24 (SAES)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s6.274,2.629,7.755,0.076 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s6.274-2.629-7.755-0.076" ;
    ;;
flashcam_grid_prod3b_north)
    CAM_ID="FlashCam"

    #GAMMA_FITS_DIR=~/data/astri_mini_array/fits/flashcam/gamma ;
    #PROTON_FITS_DIR=~/data/astri_mini_array/fits/flashcam/proton ;
    GAMMA_FITS_DIR=~/data/grid_prod3b_north/simtel/gamma ;
    PROTON_FITS_DIR=~/data/grid_prod3b_north/simtel/proton ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/flashcam_grid_prod3b_north_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="8" ; # CTA Abelardo 1st pass
    #TC_LTH="4" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="5" ;   # CTA Abelardo 2nd pass
    TC_LTH="2.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2017/07 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s4,4,5,4 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s4-4-5-4" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s4.5,4.5,4.5,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s4.5-4.5-4.5-1" ;
    ;;
nectarcam_grid_prod3b_north)
    CAM_ID="NectarCam"

    #GAMMA_FITS_DIR=~/data/grid_prod3b_north/fits/nectarcam/gamma ;
    #PROTON_FITS_DIR=~/data/grid_prod3b_north/fits/nectarcam/proton ;
    GAMMA_FITS_DIR=~/data/grid_prod3b_north/simtel/gamma ;
    PROTON_FITS_DIR=~/data/grid_prod3b_north/simtel/proton ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/nectarcam_grid_prod3b_north_cdf_gamma_mars_like.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="8" ;  # CTA Abelardo 1st pass
    #TC_LTH="4" ;  # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ;  # CTA Abelardo 2nd pass
    #TC_LTH="2" ;  # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="5" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LTH="1" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LABEL="Tailcut-BF1-${TC_HTH}-${TC_LTH}" ;

    ## 2017/08
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,4.5,3.5,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-4.5-3.5-3" ;

    ## 2017/09/07 (BF res0.5) (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,2.5,4,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-2.5-4-1" ;

    # 2017/10/24 (SAES)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s13.013,2.549,6.559,1.412 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s13.013-2.549-6.559-1.412" ;
    ;;
lstcam_grid_prod3b_north)
    CAM_ID="LSTCam"

    GAMMA_FITS_DIR=/dev/shm/.jd/lstcam/gamma ;
    #GAMMA_FITS_DIR=~/data/grid_prod3b_north/fits/lst/gamma ;
    PROTON_FITS_DIR=~/data/grid_prod3b_north/fits/lst/proton ;
    #GAMMA_FITS_DIR=~/data/grid_prod3b_north/simtel/gamma ;
    #PROTON_FITS_DIR=~/data/grid_prod3b_north/simtel/proton ;

    WT_NAN_NOISE_CDF_FILE=./pywicta/denoising/cdf/lstcam_grid_prod3b_north_cdf_gamma_mars_like.json ;

    # TAILCUT #################################################################

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="6" ; # CTA Abelardo 1st pass
    TC_LTH="3" ; # CTA Abelardo 1st pass
    TC_LABEL="Tailcut-CTA1_${TC_HTH}_${TC_LTH}_clusters-off" ;
    TC_EXTRA_OPT="--clusters=off" ;

    #TC_HTH="6" ; # CTA Abelardo 1st pass
    #TC_LTH="3" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1_${TC_HTH}_${TC_LTH}_clusters-scipy" ;
    #TC_EXTRA_OPT="--clusters=scipy" ;

    #TC_HTH="6" ; # CTA Abelardo 1st pass
    #TC_LTH="3" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1_${TC_HTH}_${TC_LTH}_clusters-mars" ;
    #TC_EXTRA_OPT="--clusters=mars" ;

    #TC_HTH="4" ; # CTA Abelardo 2nd pass
    #TC_LTH="2" ; # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2018/04/09
    #TC_HTH="6.5" ; # BF optimized
    #TC_LTH="4.5" ; # BF optimized
    #TC_LABEL="Tailcut-run18-${TC_HTH}-${TC_LTH}" ;

    ## 2018/04/09
    #TC_HTH="5.5" ; # BF optimized
    #TC_LTH="1" ;   # BF optimized
    #TC_EXTRA_OPT="--kill-isolated-pixels" ;
    #TC_LABEL="Tailcut-run19-${TC_HTH}-${TC_LTH}" ;

    ## 2018/04/09
    #TC_HTH="7" ;   # BF optimized
    #TC_LTH="4.5" ; # BF optimized
    #TC_LABEL="Tailcut-run20-${TC_HTH}-${TC_LTH}" ;

    ## 2018/04/09
    #TC_HTH="5.5" ; # BF optimized
    #TC_LTH="1" ;   # BF optimized
    #TC_LABEL="Tailcut-run21_${TC_HTH}_${TC_LTH}_clusters-mars" ;
    #TC_EXTRA_OPT="--clusters=mars" ;

    # MR_FILTER ###############################################################

    # 2017/08 (presented in LaPalma CTA meeting 2017-11-05)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,4.5,3.5,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-4.5-3.5-3" ;

    ## 2017/09/07 (BF res0.5)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2.5,4,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2.5-4-1" ;

    ## 2017/10/24 (SAES)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s23.343,2.490,-2.856,-0.719 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s23.343-2.490--2.856--0.719" ;

    ## 2018/04/09
    #WT_MRF_PARAMS="-K -k -C1 -m3 -s9,3,4 --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-s9-3-4-nk" ;

    ## 2018/04/09
    #WT_MRF_PARAMS="-K -k -C1 -m3 -s2,1,4 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-s2-1-4" ;

    # MR_TRANSFORM ############################################################

    ## 2018/04/09
    #WT_TH1="3" ;
    #WT_TH2="0" ;
    #WT_MRT_PARAMS="-f hard_filtering -t ${WT_TH1},${WT_TH2} -L drop --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_${WT_TH1}_${WT_TH2}_-L_drop--kill-isolated-pixels" ;

    # 2018/04/12
    WT_TH1="3" ;
    WT_TH2="0.2" ;
    WT_MRT_PARAMS="-f cluster_filtering -t ${WT_TH1},${WT_TH2} -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_cluster_filtering_-t_${WT_TH1}_${WT_TH2}_-L_mask" ;
    ;;
*)
    echo "Unknown option" ;
    exit 1
    ;;
esac

TC_PARAMS="-T${TC_HTH} -t${TC_LTH} ${TC_EXTRA_OPT}" ;

echo "TC_PARAMS: ${TC_PARAMS}"
echo "TC_LABEL:  ${TC_LABEL}"
echo "WT_MRF_PARAMS: ${WT_MRF_PARAMS}"
echo "WT_MRF_LABEL:  ${WT_MRF_LABEL}"
echo "WT_MRT_PARAMS: ${WT_MRT_PARAMS}"
echo "WT_MRT_LABEL:  ${WT_MRT_LABEL}"

echo "GAMMA_FITS_DIR:  ${GAMMA_FITS_DIR}"
echo "PROTON_FITS_DIR: ${PROTON_FITS_DIR}"

echo "WT_NAN_NOISE_CDF_FILE: ${WT_NAN_NOISE_CDF_FILE}"

if [ ! -d "${GAMMA_FITS_DIR}" ]
then
    echo "*** WARNING: CANNOT READ ${GAMMA_FITS_DIR} ***"
    exit 1
fi

if [ ! -d "${PROTON_FITS_DIR}" ]
then
    echo "*** WARNING: CANNOT READ ${PROTON_FITS_DIR} ***"
    exit 1
fi

# RUN DENOISING ###############################################################

sleep 5

####################
## ALL GAMMAS ######
####################
#
#echo "* NULL (REF.)"  & ./pywicta/denoising/null_ref.py             -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Ref"                      -o score_gamma_ref.json          ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_ref.json.log ;
#echo "* NULL (INPUT)" & ./pywicta/denoising/null.py                 -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Input"                    -o score_gamma_input.json        ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_input.json.log ;
#echo "* GAMMA TC"     & ./pywicta/denoising/tailcut.py              -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${TC_LABEL}" ${TC_PARAMS} -o score_gamma_${TC_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${TC_LABEL}.json.log ;
#echo "* GAMMA WT MRF" & ./pywicta/denoising/wavelets_mrfilter.py    -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRF_LABEL}" ${WT_MRF_PARAMS} -o score_gamma_${WT_MRF_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_MRF_LABEL}.json.log ;
echo "* GAMMA WT MRT" & ./pywicta/denoising/wavelets_mrtransform.py -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRT_LABEL}" ${WT_MRT_PARAMS} -o score_gamma_${WT_MRT_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_MRT_LABEL}.json.log ;
#
#####################
## ALL PROTONS ######
#####################
#
#echo "* NULL (REF.)"   & ./pywicta/denoising/null_ref.py             -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Ref"                      -o score_proton_ref.json         ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_ref.json.log ;
#echo "* NULL (INPUT)"  & ./pywicta/denoising/null.py                 -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Input"                    -o score_proton_input.json       ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_input.json.log ;
#echo "* PROTON TC"     & ./pywicta/denoising/tailcut.py              -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${TC_LABEL}" ${TC_PARAMS} -o score_proton_${TC_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${TC_LABEL}.json.log ;
#echo "* PROTON WT MRF" & ./pywicta/denoising/wavelets_mrfilter.py    -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRF_LABEL}" ${WT_MRF_PARAMS} -o score_proton_${WT_MRF_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_MRF_LABEL}.json.log ;
#echo "* PROTON WT MRT" & ./pywicta/denoising/wavelets_mrtransform.py -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRT_LABEL}" ${WT_MRT_PARAMS} -o score_proton_${WT_MRT_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_MRT_LABEL}.json.log ;
