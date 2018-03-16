#!/bin/bash

PDIR=`pwd`
SUBJECT=$(basename $PDIR)

echo -e "\nDoing some cleanup.\n"

# RAW multiband
RAWFILES=$(find ./ -name "*data" -o -name "*prep" -o -name "*ctrl" | grep -v raw/pfiles)

if [ ! -z "${RAWFILES}" ]
then
	mkdir -p ./raw/pfiles
fi

echo -e "\nMoving raw files..."
for RAWFILE in $RAWFILES
do
	BASEFILE=$(basename $RAWFILE)
	RUNNAME=$(echo $RAWFILE | awk -F/ '{print $(NF-1)}')
	TASK=$(echo $RAWFILE | awk -F/ '{print $(NF-2)}')
	NEWNAME="${SUBJECT}_${TASK}_${RUNNAME}_${BASEFILE}"
	echo mv $RAWFILE ./raw/pfiles/$NEWNAME
	mv $RAWFILE ./raw/pfiles/$NEWNAME
done


# Physio
echo -e "\nMoving physio files..."
PHYSFILES=$(find ./func/ -name "*Resp.dat" -o -name "*ECG.dat" -o -name "*resp.dat" -o -name "PPG*" -o -name "RESP*")
if [ ! -z "${PHYSFILES}" ]
then
	mkdir -p ./raw/physio/
	# echo mv $PHYSFILES ./raw/physio/
	mv $PHYSFILES ./raw/physio/
fi

# DTI
if [ -d dti ]
then
	mv dti DTI
fi

#TODO
# EPI dicoms?  
# flex.pdf
# gzip?
