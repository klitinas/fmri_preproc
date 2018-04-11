#!/bin/bash

if [ -d dicom ]
then
	DCMFILE=$(find ./dicom/ -type f -name "i*MRDC*" | head -n1)
else
	echo -e "\nNo dicom directory found?  Exiting.\n"
	exit
fi

DCMPROTOCOL=$(dcmdump $DCMFILE | grep -i protocol |  cut -d "[" -f2 | cut -d "]" -f1)
PROTOCOLSTR=$(dcmdump $DCMFILE | grep -i protocol |  cut -d "[" -f2 | cut -d "]" -f1 | sed 's/ //g' | sed 's|\/||g')

# Default place to look for config files
if [ -z "${CONFIGPATH}" ]
then
	CONFIGPATH=/export/subjects/fmri_preproc
fi

echo -e "\nLooking in ${CONFIGPATH} for config file to use.\n"

if [ ! -d "${CONFIGPATH}" ]
then
	echo -e "\nError:  ${CONFIGPATH}: no such path.\n"
	exit
fi

CONFIGFILE=$(ls ${CONFIGPATH}/${PROTOCOLSTR}*config.json 2>/dev/null)
NFILES=$(echo $CONFIGFILE | wc -w)
if [ $NFILES -ne 1 ]
then
	echo -e "\nError:  Looking for exactly 1 config file, found ${NFILES}.\n"
	exit
fi

echo -e "\n... Using ${CONFIGFILE}.\n"

echo -e "\nCreating rawdata.json\n"
read_raw_cross_ref.py raw/raw_data_cross_reference.dat 

echo -e "\nCreating the process file.\n"
write_master_process_json.py rawdata.json $CONFIGFILE

echo -e "\nDone."
