#!/bin/bash


# help text
if [ $# -eq 0 ]
then
    echo -e "\n$(basename $0): wrapper to run multiband fieldmap correction and realignment"
    echo -e "\nUSAGE: $(basename $0) -s <SUBJDIR> [options]"
    echo -e "\nAvailable options:"
    echo -e "\t-p <prep> \t\tuse 1 to prep the field maps, 0 if that's already done (default 1)"
    echo -e "\nAuthor  : Krisanne Litinas\n"
    echo -e "Revision$Id: multiband_fieldmap_correct_subject.sh 1875 2018-01-05 20:26:20Z klitinas $\n"    
    exit
fi

echo -e "\n`date`: Starting processing.\n"
echo -e "\n\nExecuting:\n$0 $*\n\n"

echo -e "Revision$Id: multiband_fieldmap_correct_subject.sh 1875 2018-01-05 20:26:20Z klitinas $\n"

# Defaults
PREP=1


# Parse options
while [ $# -gt 0 ]
do
  case $1 in
    -s)
      SUBJDIR=$2
      shift 2
      ;;
    -p)
      PREP=$2
      shift 2
      ;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done


cd $SUBJDIR
PDIR=`pwd`


if [ $PREP -eq 1 ]
then

	# Prep all the field maps
	if [ -d func/fieldmaps ]
	then
		cd func/fieldmaps
		FMDIRS=$(ls -d FM_*)

		NUMFM=$(echo $FMDIRS | wc -w)
		echo -e "\nDoing prep work for ${NUMFM} field map directories.\n"

		for FMDIR in $FMDIRS
		do
			echo -e "\n\t${FMDIR}"
			cd $FMDIR/dicom
			fieldmap_prep.sh
			cd ../..
		done
		cd $PDIR
	fi
fi



# Now do the correction on all the runs
RUNDIRS=$(find func/ -type d -name "run_*")
for RUNDIR in $RUNDIRS
do
	cd $RUNDIR
	echo -e "\nWorking in ${RUNDIR}.\n"
	TASK=$(basename `dirname $RUNDIR`)
	FMDIR=$PDIR/func/fieldmaps/FM_$TASK

	# If told not to prep fieldmaps but none exist, try it now.
	if [ ! -f $FMDIR/dicom/fpm0000.img ]
	then
		echo -e "\nFieldmap files not found, doing prep.\n"
		CURDIR=`pwd`
		cd $FMDIR/dicom
		fieldmap_prep.sh
		cd $CURDIR
	fi

	fieldmap_correct.sh -f t*run_*.nii -d $FMDIR/dicom
	cd $PDIR
done
