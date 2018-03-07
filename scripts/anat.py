#!/usr/bin/env python

from sys import argv
import subprocess
import os
import json
import shutil

## Can this be combined with func/dti?

def run_module(RAWDATA,MODULE,PARAMS):

    CMD,OUTDATA = make_script_call(RAWDATA,MODULE,PARAMS)
    subprocess.call(CMD,shell=True)
    return(OUTDATA)



# Parse params and return script call string
def make_script_call(INDATA,MODULE,PARAMS):
    OUTSTR=""
    OUTDATA=""

    if MODULE.lower() == 'dcm2nii':
        OUTDATA = '{}.nii'.format(os.path.basename(os.getcwd()))
        if PARAMS:
            OUTDATA = PARAMS['outfile']

        # Copy dicoms over to ./dicom - leave here or move into module script?
        OUTSTR = 'dcm2nii_series.sh -d {} -o {}'.format(INDATA,OUTDATA)
        shutil.copytree(INDATA,'dicom')

    elif MODULE.lower() == 'spm2_hcorr':
        OUTSTR = 'spm2_hcorr.bash -f {}'.format(INDATA)
        OUTDATA = 'h' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

    elif MODULE.lower().startswith('fsl_bet'):
        OUTSTR = 'bet_skullstrip.bash -f {}'.format(INDATA)
        OUTDATA = 'e' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

    print(OUTSTR)
    return OUTSTR, OUTDATA

# Stub to get input of a module
def generate_raw_input():
    return TRUE
# Stub to get output of a module
def generate_module_output():
    return TRUE

def preproc(JSON):
    print('Starting preprocessing on anatomy series')

    PDIR = os.getcwd()

    NUMSERIES = len(JSON)
    print('\n... {} series types found.'.format(NUMSERIES))

    # like 't1overlay_43sl'
    for SERIESTYPE in JSON.keys():
        print('\n{}'.format(SERIESTYPE))

        for SE_INFO in JSON[SERIESTYPE]:
            os.chdir(PDIR)

            RAWDATA = SE_INFO['rawdata']
            MODULES = SE_INFO['module_order']
            MODULE_PARAMS = SE_INFO['module_params']

            print('\nStarting processing on {}...\n'.format(RAWDATA))
            print('Attempting the following modules:\n')
            print('   ---\t'.join(SE_INFO['module_order']))

            # Here, make the series directory?
            # Absolute path for now?
            WORKINGDIR = '{}/anatomy/{}'.format(os.getcwd(),SERIESTYPE)
            print("Working directory: {}".format(WORKINGDIR))

            if not os.path.isdir(WORKINGDIR):
                os.makedirs(WORKINGDIR)

            # Absolute path of DCMDIR since we're changing into WORKINGDIR
            RAWDATA = os.path.abspath('dicom/{}'.format(RAWDATA))
            os.chdir(WORKINGDIR)

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
