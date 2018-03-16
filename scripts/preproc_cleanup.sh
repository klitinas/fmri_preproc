#!/bin/bash

PDIR=`pwd`
SUBJECT=$(basename $PDIR)


# RAW multiband
RAWFILES=$(find ./ -name "*data" -o -name "*prep" -o -name "*ctrl")

if [ ! -z "${RAWFILES}" ]
then
	echo mkdir -p ./raw/pfiles
fi

for RAWFILE in $RAWFILES
do
	BASEFILE=$(basename $RAWFILE)
	RUNNAME=$(echo $RAWFILE | awk -F/ '{print $(NF-1)}')
	TASK=$(echo $RAWFILE | awk -F/ '{print $(NF-2)}')
	NEWNAME="${SUBJECT}_${TASK}_${RUNNAME}_${BASEFILE}"
	echo mv $RAWFILE ./raw/pfiles/$NEWNAME
done


# Physio
PHYSFILES=$(find ./func/ -name "*Resp.dat" -o -name "*ECG.dat" -o -name "*resp.dat")
if [ ! -z "${PHYSFILES}" ]
then
	mkdir -p ./raw/physio/
	echo mv $PHYSFILES ./raw/physio/
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
