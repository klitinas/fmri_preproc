#!/usr/bin/env python

from sys import argv
import json
import os
import anat

PROCFILE = argv[1]

with open(PROCFILE) as f:
	JPROC = json.load(f)

if 'anat' in JPROC.keys():
	anat.preproc(JPROC['anat']) 

if 'func' in JPROC.keys():
    print("func.preproc(JPROC['func'])")
