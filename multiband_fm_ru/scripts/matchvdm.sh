#!/bin/bash


# help text
if [ $# -eq 0 ]
then
    echo -e "\n$(basename $0): generates vdm for a given run nii and field map"
    echo -e "\nUSAGE: $(basename $0) -f <RUNNII> [options]"
    echo -e "\nAvailable options:"
    echo -e "\t-fm <fmfile> \t\t.img generated from fieldmap_prep.sh (default fpm000.img)"
    echo -e "\t-t <TERT> \t\tstudy-specific value"
    echo -e "\t-mag <fm mag. image> \t.nii generated from fieldmap_prep.sh (default my_fieldmap_mag_brain.nii)"
    echo -e "\nAuthor  : Krisanne Litinas\n"
    echo -e "Revision$Id: matchvdm.sh 1873 2018-01-05 20:25:15Z klitinas $\n"    
    exit
fi

echo -e "\nExecuting: $0 $*\n"


PDIR=`pwd`

# Defaults
FMFILE=fpm0000.img
RUNNII=run_01.nii
TERT=48.24
MAGFILE=my_fieldmap_mag_brain.nii
BLIPDIR=+1

#if [ -z "echo ${SPM12PATH}" ]
if [ -z "${SPM12PATH}" ]
then
  SPM12PATH=/export/prog/spm/spm12
fi


# Parse options
while [ $# -gt 0 ]
do
  case $1 in
    -fm)
      FMFILE=$2
      shift 2
      ;;
    -t)
      TERT=$2
      shift 2
      ;;
	-mag)
	  MAGFILE=$2
	  shift 2
      ;;
	-f)
	  RUNNII=$2
	  shift 2
	  ;;
  -b)
    BLIPDIR=$2
    shift 2
    ;;
    *)
      echo -e "\nUnknown option: $1. Exiting.\n"
      exit
      ;;
  esac
done


echo -e "\nCreating VDM file...\n"
matlab -nosplash -nodesktop << EOF

	% Fix for specific machine
	%addpath('/export/prog/spm/spm12')
	addpath('${SPM12PATH}')
	%addpath('/export/prog/spm/spm12/toolbox/FieldMap')
	addpath('${SPM12PATH}/toolbox/FieldMap')
	IP = FieldMap('Initialise'); % Gets default params from pm_defaults

	%fm = 'fpm0000.img';
	fm = '${FMFILE}';
	IP.pP = spm_vol(fm);
	IP.fm.fpm = spm_read_vols(IP.pP);
	IP.fm.jac = pm_diff(IP.fm.fpm,2);

	%IP.blipdir = +1;
	IP.blipdir = $BLIPDIR;

	% scp
	% IP.tert = 51.84;            % verify this
	IP.tert = $TERT

	[IP.vdm, IP.vdmP]=FieldMap('FM2VDM',IP);
	
	epiP = spm_vol('${RUNNII}');
	%IP.epiP = epiP(1);
	IP.epiP = epiP(10);

	%IP.fmagP = spm_vol('my_fieldmap_mag_brain.nii');
	IP.fmagP = spm_vol('${MAGFILE}');
	IP.vdmP = FieldMap('MatchVDM',IP); %magnitude image here?
	
EOF
