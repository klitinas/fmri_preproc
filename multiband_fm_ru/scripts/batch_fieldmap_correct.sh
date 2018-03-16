#!/bin/bash

cd /export/archive/trailer

SUBJECTS=$(ls -d kdf*)

for SUBJ in $SUBJECTS
do
	multiband_fieldmap_correct_subject.sh $SUBJ > $SUBJ_fm_correct.log
done
