#!/bin/bash

# help text
if [ $# -eq 0 ]
then
  echo -e "\n$(basename $0): wrapper to dcm2nii"
  echo -e "\nUSAGE: $(basename $0) -d <DCMDIR> [options]"
  echo -e "\nAvailable options:"
  echo -e "\t-o <OUTFILE> \t\tname of output .nii"
  echo -e "\nAuthor  : Krisanne Litinas"
  echo -e "Revision$Id$\n"
  exit
fi

echo -e "\n\nExecuting:\n$0 $*\n\n"

# Defaults
DCMDIR=`pwd`
OUTFILE='out.nii'

SCRIPTSDIR=$(dirname $0)
PATH=$PATH:$SCRIPTSDIR

# Parse options
while [ $# -gt 0 ]
do
  case $1 in
    -d)
      DCMDIR=$2
      shift 2
      ;;
    -o)
      OUTFILE=$2
      shift 2
      ;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done

# Checks
# Check that directory exists

# Get absolute path of desired output file
PDIR=`pwd`
dcm2nii -g N -p N -d N -x N -r N -c N $DCMDIR/

# TO DO:  account for differing dcm2nii output .nii names (can there be more possibilities?)
if [ -f $DCMDIR/s*a1001.nii ]
then
	mv $DCMDIR/s*a1001.nii $OUTFILE
else
	mv $DCMDIR/s*a1002.nii $OUTFILE
fi
