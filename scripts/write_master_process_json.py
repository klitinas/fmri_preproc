#!/usr/bin/env python

from sys import argv
import json
import os
import copy

def get_json(FILENAME):
    with open(FILENAME) as f:
        return json.load(f)

def count_sedesc(d,SEDESC):
    c = 0
    for dd in d.keys():
        if d[dd]['sedesc'].lower() == SEDESC.lower():
            c+=1

    return c    

def proc_dict(CDAT,RDAT):
    PROC_OUT = {}

    for SENUM in sorted(RDAT.keys()):
        RAWDATA = RDAT[SENUM]['rawdata']
        SEDESC = RDAT[SENUM]['sedesc']

        SE_OUT = {}

        if SEDESC not in CDAT:
            continue

        CFG_SERIES = CDAT[SEDESC]

        SE_OUT['rawdata'] = RAWDATA

        if 'module_order' in CFG_SERIES.keys():
            SE_OUT['module_order'] = CFG_SERIES['module_order']

        if 'module_params' in CFG_SERIES.keys():
            SE_OUT['module_params'] = copy.deepcopy(CFG_SERIES['module_params'])

        if 'acqtype' in RDAT[SENUM].keys():
            SE_OUT['acqtype'] = RDAT[SENUM]['acqtype']

        if 'phys_files' in RDAT[SENUM].keys():
            SE_OUT['phys_files'] = RDAT[SENUM]['phys_files']


        if SEDESC.lower().startswith('func_') or SEDESC.lower().startswith('dti_'):
            SE_OUT['run_name'] = 'run_01'
            if SEDESC in PROC_OUT.keys():
                RUNNUM = len(PROC_OUT[SEDESC]) + 1
                RUNNAME = 'run_{:02d}'.format(RUNNUM)

                SE_OUT['run_name'] = RUNNAME


		# Account for if multiple series of given anatomy scan run
        if SEDESC.lower().startswith('t1') or SEDESC.lower().startswith('t2') or SEDESC.lower().startswith('vasc'):
            if count_sedesc(RDAT,SEDESC) > 1:
                RUNNAME = '{}_s{}'.format(SEDESC.lower(),SENUM)
                SE_OUT['run_name'] = RUNNAME 

                if 'dcm2nii' in SE_OUT['module_order']:
					if 'module_params' not in SE_OUT.keys():
						SE_OUT['module_params'] = {}
						SE_OUT['module_params']['dcm2nii'] = {}
					#SE_OUT['module_params']['dcm2nii']['outname'] = RUNNAME + '.nii'
					SE_OUT['module_params']['dcm2nii']['outname'] = RUNNAME + '.nii'
        
        # Append to list if not exist
        PROC_OUT.setdefault(SEDESC, []).append(SE_OUT)


    return PROC_OUT

# Adding this for fieldmap dicoms
def proc_dict_fm(CDAT,RDAT):
    PROC_OUT = {}
    for SENUM in sorted(RDAT.keys()):

        RAWDATA = RDAT[SENUM]['rawdata']
        SEDESC = RDAT[SENUM]['sedesc']

        SE_OUT = {}

        SE_OUT['rawdata'] = RAWDATA
        SE_OUT['sedesc'] = SEDESC

        SE_OUT['module_order'] = ['cp_fieldmap_dcms','fieldmap_prep']

        # Append to list if not exist
        PROC_OUT.setdefault(SEDESC, []).append(SE_OUT)

    return PROC_OUT

RAWFILE = argv[1]
CONFIGFILE = argv[2]

# Read the raw cross ref and config files
DAT_RAW = get_json(RAWFILE)
DAT_CFG = get_json(CONFIGFILE)

# Loop through the series types (TO DO: DTI non-mb)
DOUT = {}
if 'anat' in DAT_RAW.keys():
    DOUT['anat'] = proc_dict(DAT_CFG,DAT_RAW['anat'])

if 'func' in DAT_RAW.keys():
    DOUT['func'] = proc_dict(DAT_CFG,DAT_RAW['func'])

if 'func_fieldmap' in DAT_RAW.keys():
    DOUT['func_fieldmap'] = proc_dict_fm(DAT_CFG,DAT_RAW['func_fieldmap'])

if 'dti' in DAT_RAW.keys():
    DOUT['dti'] = proc_dict(DAT_CFG,DAT_RAW['dti'])

# Write out the json
jfid = open('master_process_out.json','w')
json_data = json.dumps(DOUT, ensure_ascii=False)
python_obj = json.loads(json_data)
jfid.write(json.dumps(python_obj, sort_keys=True, indent=4))
jfid.close()
