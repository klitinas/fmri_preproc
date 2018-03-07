#!/usr/bin/env python

from sys import argv
import subprocess
import os
import json
import shutil

## Can this be combined with func/dti?

def run_module(RAWDATA,MODULE,PARAMS):

    CMD,OUTDATA = make_script_call(RAWDATA,MODULE,PARAMS)
    #subprocess.call(CMD,shell=True)
    print(CMD)
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

    elif MODULE.lower() == 'recon_multiband':
        if PARAMS:
            print(PARAMS)            
 
        OUTDATA = os.path.basename(os.path.dirname(INDATA)) + '.nii'       
        OUTSTR = 'mux_recon_func.bash -f {} -h -o {}'.format(INDATA,OUTDATA)

    elif MODULE.lower() == "slicetiming_spm8_multiband":
        OUTSTR = 'multiband_spm8_slicetiming.bash -f {}'.format(INDATA)
        OUTDATA = 't' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

    elif MODULE.lower() == "epi_fm_realign_unwarp":
        OUTSTR = ""
        OUTDATA = ""

    elif MODULE.lower() == "retroicor_multiband":
        OUTSTR = 'multiband_retroicor.bash -f {}'.format(INDATA)
        OUTDATA = 'p' + INDATA
        if PARAMS:
            if 'prefix' in PARAMS:
                PREFIX = PARAMS['prefix']
                OUTSTR += ' -p {}'.format(PREFIX)
                OUTDATA = PREFIX + INDATA

    elif MODULE.lower() == "fsl_mcflirt_realign":
        OUTSTR = ""
        OUTDATA = ""

    elif MODULE.lower() == "despike":
        OUTSTR = ""
        OUTDATA = ""

    else:
        OUTSTR='test'

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

            if SERIESTYPE.lower().startswith('func_'):
                TASK = SERIESTYPE.lower().split('_')[1]
                RUNNAME = SE_INFO['run_name']
                WORKINGDIR = '{}/func/{}/{}'.format(os.getcwd(),TASK,RUNNAME)

                # Absolute path of DCMDIR since we're changing into WORKINGDIR
                # Depends on acqtype:
                    # Spiral in raw/pfiles
                    # Conv. EPI in dicom/
                    # Multiband EPI in func/task/run_name/

                if SE_INFO['acqtype'] == 'spiral':
                    RAWDATA = os.path.abspath('{}/raw/pfiles/{}'.format(os.getcwd(),RAWDATA))
                elif SE_INFO['acqtype'] == 'multiband':
                    RAWDATA = os.path.abspath('{}/func/{}/{}/{}'.format(os.getcwd(),TASK,RUNNAME,RAWDATA))
                elif SE_INFO['acqtype'] == 'epi':
                    RAWDATA = os.path.abspath('dicom/{}'.format(RAWDATA))
					
            else:
                WORKINGDIR = '{}/anatomy/{}'.format(os.getcwd(),SERIESTYPE)

            	# Absolute path of DCMDIR since we're changing into WORKINGDIR
            	RAWDATA = os.path.abspath('dicom/{}'.format(RAWDATA))

            print("Working directory: {}".format(WORKINGDIR))

            if not os.path.isdir(WORKINGDIR):
                os.makedirs(WORKINGDIR)

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

    if 'func' in JSON.keys():
        JSON = JSON['func']

    preproc(JSON)
