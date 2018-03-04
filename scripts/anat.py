#!/usr/bin/env python

from sys import argv
import subprocess
import os
import json

def run_module(RAWDATA,MODULE,PARAMS):
    print(MODULE)
    print(PARAMS)

    CMD,OUTDATA = make_script_call(RAWDATA,MODULE,PARAMS)
    return(OUTDATA)


# Parse params and return script call string
def make_script_call(INDATA,MODULE,PARAMS):
    if MODULE.lower() == 'dcm2nii':
        OUTSTR = 'run_dcm2nii.sh dicom/{}'.format(INDATA)
        OUTDATA = 't1overlay.nii'
        return OUTSTR, OUTDATA

    elif MODULE.lower() == 'spm2_hcorr':
        OUTSTR = 'spm2_hcorr -f {}'.format(INDATA)
        OUTDATA = 'h' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

        return OUTSTR, OUTDATA

    elif MODULE.lower().startswith('fsl_bet'):
        OUTSTR = 'bet_skullstrip -f {}'.format(INDATA)
        OUTDATA = 'e' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

        return OUTSTR, OUTDATA

# Stub to get input of a module
def generate_raw_input():
    return TRUE
# Stub to get output of a module
def generate_module_output():
    return TRUE

def preproc(JSON):
    print('Starting preprocessing on anatomy series')
    NUMSERIES = len(JSON)
    print('\n... {} series types found.'.format(NUMSERIES))

    # like 't1overlay_43sl'
    for SERIESTYPE in JSON.keys():
        print('\n{}'.format(SERIESTYPE))

        for SE_INFO in JSON[SERIESTYPE]:

            RAWDATA = SE_INFO['rawdata']
            MODULES = SE_INFO['module_order']
            MODULE_PARAMS = SE_INFO['module_params']

            print('\nStarting processing on {}...\n'.format(RAWDATA))
            print('Attempting the following modules:\n')
            print('   ---\t'.join(SE_INFO['module_order']))

            WORKINGDATA = RAWDATA
            for MODULE in MODULES:
                if MODULE in MODULE_PARAMS.keys():
                    THIS_MODULE_PARAMS = MODULE_PARAMS[MODULE]
                else:
                    THIS_MODULE_PARAMS = {}

                WORKINGDATA = run_module(WORKINGDATA,MODULE,THIS_MODULE_PARAMS)




if __name__ == '__main__':

    # anat.py executed as script
    with open(argv[1]) as f:
        JSON = json.load(f)

    if 'anat' in JSON.keys():
        JSON = JSON['anat']

    preproc(JSON)
