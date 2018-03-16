#!/bin/bash

# help text
if [ $# -eq 0 ]
then
    echo -e "\n$(basename $0): wrapper to do multiband field correction."
    echo -e "\nUSAGE: $(basename $0) -f <NIIFILETOCORRECT> [options]"
    echo -e "\nAvailable options:"
    echo -e "\t-d <DCMDIR> \t\tdirectory containing field map dicoms (default pwd)\n"
    exit
fi

echo -e "\nExecuting: $0 $*\n"


PDIR=`pwd`

# Defaults
DCMDIR=$PDIR
RUNNII=run_01.nii

# Parse options
while [ $# -gt 0 ]
do
  case $1 in
    -f)
      RUNNII=$2
      shift 2
      ;;
    -d)
      DCMDIR=$2
      shift 2
      ;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done


echo -e "\nAttempting correction on ${RUNNII}.\n"
echo -e "\nPrepping the process.\n"

# Make temporary copy of .nii into dicom directory 
# Change into dicom directory and start the prep.

RUNDIR=$(dirname $RUNNII)
BSERUN=$(basename $RUNNII)

cd $RUNDIR
RUNDIR=`pwd`
cd $PDIR

#cp -p $RUNNII $DCMDIR/
cd $DCMDIR
#fieldmap_prep.sh $RUNDIR/$RUNNII

cd $PDIR

echo -e "\nRunning realign/unwarp job.\n"
fm_realign_unwarp.sh -f $RUNNII -vdm $DCMDIR/vdm5_fpm0000.img
