#!/bin/bash

# help text
if [ $# -eq 0 ]
then
    echo -e "\n$(basename $0): wrapper to do multiband field correction."
    echo -e "\nUSAGE: $(basename $0) -f <NIIFILETOCORRECT> [options]"
    echo -e "\nAvailable options:"
    echo -e "\t-d <DCMDIR> \t\tdirectory containing field map dicoms (default pwd)"
    echo -e "\t-t <TERT> \t\tcontains timing value in ms derived from eht, etl CVs used to create vdm (default 48.24)\n"
    echo -e "\nAuthor  : Krisanne Litinas\n"
    echo -e "Revision$Id: fieldmap_correct.sh 1872 2018-01-05 20:24:00Z klitinas $\n"    
    exit
fi

echo -e "\nExecuting: $0 $*\n"


PDIR=`pwd`

# Defaults
DCMDIR=$PDIR
RUNNII=run_01.nii
TERT=""

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
	-t)
      TERT=$2
      shift 2
      ;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done


echo -e "\nAttempting correction on ${RUNNII}.\n"

# If needed, run fieldmap_prep.sh
echo -e "\nPrepping the process.\n"
if [ ! -f $DCMDIR/fpm0000.img ]
then
	TMPDIR=`pwd`
	cd $DCMDIR
	fieldmap_prep.sh
	cd $TMPDIR
fi

echo -e "\nChecking that ${RUNNII} exists...\n"

if [ -f $RUNNII ]
then
  echo -e "\tfound.\n"
else
  echo -e "\tfile not found - aborting.\n"
  exit
fi

# Change into dicom directory and run the matchvdm script.
RUNDIR=$(dirname $RUNNII)
BSERUN=$(basename $RUNNII)

cd $RUNDIR
RUNDIR=`pwd`

# Get the blip direction from the pfile header
PFILE=$(ls P*.7)
#BLIPDIR=$(head -c147732 $PFILE | tail -c4 | od -f -An | awk '{print $1}')
BLIPDIR=$(python <<EOF
import struct
f = open('${PFILE}','r')
f.seek(147732)
blipvar = struct.unpack('f', f.read(4))[0]
if blipvar == 1:
	BLIPDIR = -1
else:
	BLIPDIR = +1
f.close()
print(BLIPDIR)
EOF
)

cd $PDIR

cd $DCMDIR
#matchvdm.sh -f $RUNDIR/$RUNNII -b $BLIPDIR

# New:  allow inputs for tert (cvs etl * esp)
if [ ! -z $TERT ]
then
	matchvdm.sh -f $RUNDIR/$RUNNII -b $BLIPDIR -t $TERT
else
	matchvdm.sh -f $RUNDIR/$RUNNII -b $BLIPDIR
fi


# Move the vdm5 file from the dicom dir
mv vdm5_fpm0000* $PDIR/
cd $PDIR

# Run the realign/unwarp
echo -e "\nRunning realign/unwarp job.\n"
fm_realign_unwarp.sh -f $RUNNII -vdm vdm5_fpm0000.img
