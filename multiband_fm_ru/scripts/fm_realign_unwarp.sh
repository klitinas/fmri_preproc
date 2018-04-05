#!/bin/bash

# help text
if [ $# -eq 0 ]
then
    echo -e "\n$(basename $0): wrapper to do multiband realign/unwarp job."
    echo -e "\nUSAGE: $(basename $0) -f <NIIFILETOCORRECT> [options]"
    echo -e "\nAvailable options:"
    echo -e "\t-vdm <VDMFILE> \t\tvdm file to use (default vdm5_fpm0000.img)\n"
    echo -e "\nAuthor  : Krisanne Litinas\n"
    echo -e "Revision$Id: fm_realign_unwarp.sh 1874 2018-01-05 20:25:53Z klitinas $\n"    
    exit
fi

echo -e "\n\nExecuting:\n$0 $*\n\n"

SCRIPTPATH=$(dirname $0)

if [ -z "${SPM12PATH}" ]
then
  SPM12PATH=/export/prog/spm/spm12
fi

# Defaults
VDMFILE=vdm5_fpm0000.img

# Get alignref image - if first run is missing, use the next.
REFFILE=$(find ../ -name "run*nii" | sort | head -n1)

# Parse options
while [ $# -gt 0 ]
do
  case $1 in
    -f)
      NII=$2
      shift 2
      ;;
    -vdm)
      VDMFILE=$2
      shift 2
      ;;
    -ref)
		REFFILE=$2
		shift 2
		;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done


echo -e "Running realign/unwarp job on ${NII}..\n"
echo -e "\nUsing VDM: ${VDMFILE}.\n"
echo -e "\nUsing reference image: ${REFFILE}.\n"

matlab -nosplash -nodesktop << EOF

	% Paths, probably make this automated
	addpath('${SPM12PATH}')
	addpath('${SPM12PATH}/toolbox/FieldMap/')
	addpath('${SCRIPTPATH}/../mfiles')
	
	%fm_realign_unwarp('${NII}','${VDMFILE}','../run_01/run_01.nii');	
	fm_realign_unwarp('${NII}','${VDMFILE}','${REFFILE}');	
	
EOF

echo -e "\nAll done.\n"
