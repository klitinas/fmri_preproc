#!/bin/bash

# despike.bash DespikeMatFile DespikeLogFile
# source ${thisDir}/src/despike.bash ${FullRunDir}/wpixscr.m ${FullRunDir}/wpixscr.log >> $logFile 2>&1

PFILE=$1

DespikeMatFile=$2
DespikeLogFile=$3

OutputDir=`dirname ${DespikeMatFile}`

let year=`head -c 26 $PFILE | tail -c 4`
echo "data collected in year: ${year}"
let year=${year}+1900

fastRec=0
#newdd=`echo $disdaq | awk -F"." '{ print $1 }'`
newdd=$(rawfileinfo.bash -f $PFILE | grep -i disdaq | awk '{print $2}' | awk -F. '{print $1}')
if [ $newdd -eq 0 ]
then
    skipframe=3
    ddaflag=0
     
else
     skipframe=1
     ddaflag=1
fi

#get nphases for check despiker script
#nphases=`${thisDir}/src/gspmat01.csh $ITRECPATH $PFILE V | grep -w nphases: | cut -d':' -f2`
nphases=$(rawfileinfo.bash -f $PFILE | grep -i images | awk '{print $NF}')

echo "Skipframe is: $skipframe"
echo "ddaflag is: $ddaflag"
echo "nphases from $PFILE header: $nphases"
echo "Pfile : $PFILE  Year : $year fastReceiver: $fastRec"
echo "removing white pixel artifact using despiker_interp.m ..."
echo "warning off" > ${DespikeMatFile}

#echo "addpath $MATLABPATH" >> ${DespikeMatFile}
echo "despiker_output = despiker_interp('$PFILE',3,$fastRec,$year,1)" >> ${DespikeMatFile}
echo "save('${OutputDir}/despiker_output','despiker_output')" >> ${DespikeMatFile}
echo "quit" >> ${DespikeMatFile}

#${MATLAB} -nosplash -nodisplay  -nojvm  <  ${DespikeMatFile}  > ${DespikeLogFile}
matlab -nosplash -nodisplay  -nojvm  <  ${DespikeMatFile}  > ${DespikeLogFile}
echo "Exit status is: $?"
echo "... done with white pixel correction"
echo ""


# despike output check
#source ${thisDir}/src/despikeCheckCall.bash ${FullRunDir}/checkwpixscr.m ${FullRunDir}/checkwpixscr.log >> $logFile 2>&1

#ITRECPATH=/export/home/fmrilab/krisanne_test/heitzeg_batch_recon/20160107_recon8it/mfiles
#CheckSpikeMatFile=$1
#CheckSpikeLogFile=$2
dIn=0
dOut=0
CheckSpikeMatFile=checkwpixscr.m
CheckSpikeLogFile=checkwpixscr.log
OLD_PFILE=$PFILE
PFILE=f_$PFILE

#echo "Old pfile : ${old_pfile}"
#echo "New pfile : ${pfile}"
echo "Old pfile : ${OLD_PFILE}"
echo "New pfile : ${PFILE}"
echo "checking despiked images with despiker_output check..."
echo "warning off" > ${CheckSpikeMatFile}
echo "addpath /export/krisanne/20170919_umichfmri_recon/mfiles/" >> ${CheckSpikeMatFile}
echo "additrecpaths" >> ${CheckSpikeMatFile}
#echo "addpath $ITRECPATH" >> ${CheckSpikeMatFile}
#echo "setup_path_itrec('$ITRECPATH')" >> ${CheckSpikeMatFile}
echo "despiker_output_check('$OLD_PFILE','$PFILE','$dIn', '$dOut', $nphases)" >> ${CheckSpikeMatFile}
echo 
echo "quit" >> ${CheckSpikeMatFile}

matlab -nosplash -nodisplay  -nojvm  <  ${CheckSpikeMatFile}  > ${CheckSpikeLogFile}
echo ".....done with checking spikes"
echo ""
