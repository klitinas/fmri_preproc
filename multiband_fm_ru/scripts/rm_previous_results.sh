#!/bin/bash

SUBJ=$1
cd $SUBJ

echo `pwd`


find ./func/ -name "rp_t*run*txt" | xargs rm
find ./func/ -name "vdm*img" | xargs rm
find ./func/ -name "vdm*hdr" | xargs rm
find ./func/ -name "wfmag_t*nii" | xargs rm
find ./func/ -name "ut*run*nii" | xargs rm
find ./func/ -name "meanut*run*nii" | xargs rm
find ./func/ -name "t*run*_uw.mat" | xargs rm
find ./func/ -name "tmpru*" | xargs rm
