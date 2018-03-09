#!/usr/bin/env python

from sys import argv
import json
import os

def get_json(FILENAME):
    with open(FILENAME) as f:
        return json.load(f)


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
            SE_OUT['module_params'] = CFG_SERIES['module_params']

        if 'acqtype' in RDAT[SENUM].keys():
            SE_OUT['acqtype'] = RDAT[SENUM]['acqtype']

        if 'phys_files' in RDAT[SENUM].keys():
            SE_OUT['phys_files'] = RDAT[SENUM]['phys_files']


        if SEDESC.lower().startswith('func_'):
            SE_OUT['run_name'] = 'run_01'
            if SEDESC in PROC_OUT.keys():
                RUNNUM = len(PROC_OUT[SEDESC]) + 1
                RUNNAME = 'run_{:02d}'.format(RUNNUM)

                SE_OUT['run_name'] = RUNNAME


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

        SE_OUT['module_order'] = ['cp_fieldmap_dcms']

        # Append to list if not exist
        PROC_OUT.setdefault(SEDESC, []).append(SE_OUT)   
    
    return PROC_OUT    

RAWFILE = argv[1]
CONFIGFILE = argv[2]

# Read the raw cross ref and config files
DAT_RAW = get_json(RAWFILE)
DAT_CFG = get_json(CONFIGFILE)

# Loop through the series types (TO DO: DTI)
DOUT = {}
if 'anat' in DAT_RAW.keys():
    DOUT['anat'] = proc_dict(DAT_CFG,DAT_RAW['anat'])

if 'func' in DAT_RAW.keys():
    DOUT['func'] = proc_dict(DAT_CFG,DAT_RAW['func'])

if 'func_fieldmap' in DAT_RAW.keys():
    DOUT['func_fieldmap'] = proc_dict_fm(DAT_CFG,DAT_RAW['func_fieldmap']) 

# Write out the json
jfid = open('master_process_out.json','w')
json_data = json.dumps(DOUT, ensure_ascii=False)
python_obj = json.loads(json_data)
jfid.write(json.dumps(python_obj, sort_keys=True, indent=4))
jfid.close()
