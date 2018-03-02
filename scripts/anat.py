#!/usr/bin/env python

from sys import argv
import os
import json

def run_module(MODULE,PARAMS):
    print(MODULE)
    print(PARAMS)

    # Parse PARAMS (based on each module?)

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
            print(MODULE_PARAMS)

            print('\nStarting processing on {}...\n'.format(RAWDATA))
            print('Attempting the following modules:\n')
            print('   ---\t'.join(SE_INFO['module_order']))

   
            for MODULE in MODULES:
                if MODULE in MODULE_PARAMS.keys():
                    THIS_MODULE_PARAMS = MODULE_PARAMS[MODULE]
                else:
                    THIS_MODULE_PARAMS = {}

                run_module(MODULE,THIS_MODULE_PARAMS)      

       
            
            


if __name__ == '__main__':

    # anat.py executed as script
    with open(argv[1]) as f:
        JSON = json.load(f)

    if 'anat' in JSON.keys():
        JSON = JSON['anat']
 
    preproc(JSON)
