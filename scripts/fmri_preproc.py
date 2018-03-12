#!/usr/bin/env python

from sys import argv
import json
import os
import anat
import func

PROCFILE = argv[1]

with open(PROCFILE) as f:
    JPROC = json.load(f)

if 'anat' in JPROC.keys():
	func.preproc(JPROC['anat']) 

if 'func_fieldmap' in JPROC.keys():
    func.preproc(JPROC['func_fieldmap'])

if 'func' in JPROC.keys():
    func.preproc(JPROC['func'])

if 'dti' in JPROC.keys():
    func.preproc(JPROC['dti'])
