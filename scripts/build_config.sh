#!/bin/bash

# Be in the subject directory.
PDIR=`pwd`

# Defaults
FETCH_PROTOCOL=0
OUTFILE=config.json
ACQTYPE='mb'
STUDYNAME='study'

# Parse options
while [ $# -gt 0 ] 
do
  case $1 in
    -p)
      FETCH_PROTOCOL=1
      shift 1
      ;;  
    -o) 
      OUTFILE=$2
      shift 2
      ;;  
	-aq)
		ACQTYPE=$2
		shift 2
		;;
	-s)
		STUDYNAME=$2
		shift 2
		;;
    *)  
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;  
  esac
done

if [ $FETCH_PROTOCOL -eq 1 ]
then
	DCMFILE=$(find ./dicom/ -type f -name "i*MRDC*" | head -n1)
	fetch_protocol.sh $DCMFILE
	write_config.py .protocol $ACQTYPE
	mv test_config.json $OUTFILE 2>/dev/null
fi


