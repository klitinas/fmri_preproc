#!/bin/bash

#Major code: Mike Angstadt
#Minor code: Scott Peltier, Krisanne Litinas

echo -e "\nExecuting: $0 $*\n"

echo -e "\nLooking for dicom files in `pwd`\n"


export FSLOUTPUTTYPE=NIFTI

# Convert fieldmap data to nii, then split into -1/+1 blip images
NDCMS=$(ls *MRDC* | wc -w)
echo -e "\nWorking on ${NDCMS} dicom files.\n"

echo -e "\nConverting dicoms to nifti with command:"
dicom=`ls *.MRDC.1`

echo -e "\n\tdcm2nii -g N -d N -e N ${dicom}"
dcm2nii -g N -d N -e N $dicom &>/dev/null

# Check that a .nii was created
NII=$(ls -rt *nii 2>/dev/null | tail -n1)
if [ -z "${NII}" ]
then
	echo -e "\nError: no .nii created! Exiting.\n"
	exit
fi

echo -e "\nNifti created:  ${NII}"


echo -e "\nSplitting ${NII} into 2 volumes..."
fslsplit $NII FM -t

echo -e "\nCreated:\n`ls FM*nii`\n"

cp FM0000.nii fFM0000.nii

# take care of orientation, merge data
a=`fslorient -getqform fFM0000.nii`

#need to flip sign of second row
echo -e "\nTaking care of orientation.\n"
a5=`echo $a | awk 'BEGIN { FS=" " } {print $5 "*-1"}' | bc`
a6=`echo $a | awk 'BEGIN { FS=" " } {print $6 "*-1"}' | bc`
a7=`echo $a | awk 'BEGIN { FS=" " } {print $7 "*-1"}' | bc`
a8=`echo $a | awk 'BEGIN { FS=" " } {print $8 "*-1"}' | bc`
nega=`echo $a $a5 $a6 $a7 $a8 | awk '{print $1,$2,$3,$4,$17,$18,$19,$20,$9,$10,$11,$12,$13,$14,$15,$16}'`

fslorient -setqform ${nega} fFM0000.nii 
fslorient -copyqform2sform fFM0000.nii 2>/dev/null
fslswapdim fFM0000.nii -x -y z ffFM0000.nii 

#adjust for odd number of slices by adding in extra slice
NSLICES=$(expr $NDCMS / 2)
REM=$(expr $NSLICES % 2)


if [ $REM -eq 1 ]
then
	echo -e "\nOdd number of slices detected, padding with extra slice.\n"
	cp FM0001.nii FM0001_orig.nii
	cp ffFM0000.nii ffFM0000_orig.nii

	fslroi ffFM0000.nii tmp_pe0 0 -1 0 -1 0 1 0 -1
	fslroi FM0001.nii  tmp_pe1 0 -1 0 -1 0 1 0 -1
	fslmerge -z rs_pe0 tmp_pe0 ffFM0000.nii 
	fslmerge -z rs_pe1 tmp_pe1 FM0001.nii
	fslmerge -t FM.nii rs_pe0 rs_pe1 2>/dev/null

else
	fslmerge -t FM.nii ffFM0000.nii FM0001.nii 2>/dev/null
fi

#fslmerge -t FM.nii ffFM0000.nii FM0001.nii #gives a warning here, probably ok?
#fslmerge -t FM.nii rs_pe0 rs_pe1

#get echo spacing and echo train length to calculate total readout length
#https://cni.stanford.edu/wiki/GE_Processing

es=`dicom_hdr $dicom | grep "0043 102c" | sed 's/0043 102c[ ]*[0-9] \[[0-9 ]*\] \/\/[ ]*\/\/ //'`
etl=`dicom_hdr $dicom | grep "0018 0081" | sed 's/0018 0081[ ]*[0-9] \[[0-9 ]*\] \/\/[ ]*ACQ Echo Time\/\///'`
trl=`echo "scale=4;$es * $etl / 1000 / 1000" | bc`

echo -e "\nParameters detected:"
echo -e "\n\tEcho spacing: ${es}"
echo -e "\tEcho train length: ${etl}"
echo -e "\tTotal readout length: ${trl}"

echo "0 -1 0 $trl" > datain.txt
echo "0 1 0 $trl" >> datain.txt

# call topup to get fieldmap and unwarped se_epi to get magnitude image for fieldmap

echo -e "\nDoing topup using:"
echo -e "topup --imain=FM.nii --datain=datain.txt --config=b02b0.cnf --fout=my_fieldmap --iout=se_epi_unwarped\n"
topup --imain=FM.nii --datain=datain.txt --config=b02b0.cnf --fout=my_fieldmap --iout=se_epi_unwarped

#adjust for resizing

echo -e "\nResizing.\n"
fslroi my_fieldmap myfieldmap_resized 0 -1 0 -1 1 -1 0 -1
fslroi se_epi_unwarped se_epi_unwarped_resized 0 -1 0 -1 1 -1 0 -1

#change names

fslmaths myfieldmap_resized -mul 6.28 my_fieldmap_rads   # check if needed
fslmaths se_epi_unwarped_resized -Tmean my_fieldmap_mag

bet2 my_fieldmap_mag my_fieldmap_mag_brain     

export FSLOUTPUTTYPE=NIFTI_PAIR
fslsplit myfieldmap_resized.nii fpm     # SPM needs hdr/img nifti for FieldMap toolbox

echo -e "\nDone."
