#!/usr/bin/env python

import json
import os
import subprocess
import xml.etree.ElementTree as ET
from sys import argv

PROTOCOLFILEXML = argv[1]
OUTFILE = PROTOCOLFILEXML.replace('_session.xml','_config.json')

#OUTFILE = argv[2]

# Optional input for spiral/mb type (default: mb)
if len(argv) > 2:
    ACQTYPE = argv[2]
else:
    ACQTYPE = 'multiband'


# Get list of expected runs
tree = ET.parse(PROTOCOLFILEXML)
root = tree.getroot()

LRUNS=[]
for child in root:
    if child.tag.lower().endswith('}task'):
        LRUNS.append(child.get('name'))

DOUT = {}

# Now classify into func/dti/anatomy/spectro/etc types
for RUNNAME in LRUNS:
    NRUNS = LRUNS.count(RUNNAME)

    if RUNNAME.lower() not in DOUT.keys():
        if RUNNAME.lower().startswith('func_'):
            DOUT[RUNNAME.lower()] = {}
            D_THISTYPE = {}
            D_THISTYPE['nreps'] = NRUNS

            TASK = RUNNAME.lower().split('_')[1]

            # Account for multiband/spiral/convEPI types
            # TODO: how to put in physio correction?
            if ACQTYPE.lower() == 'mb':
                FMNAME = "FM_{}".format(TASK)
                D_THISTYPE['module_order'] = ["recon_multiband","retroicor_multiband","slicetiming_spm8_multiband","epi_fm_realign_unwarp"]
                D_THISTYPE['module_params'] = {"epi_fm_realign_unwarp":{"tert": 48.24,"fm_name": FMNAME}}

            elif ACQTYPE.lower() == 'spiral':
                D_THISTYPE['module_order'] = ["despike","recon_cprec","retroicor","slicetiming_spm8","mcflirt_fsl_v5.0.x"]

            DOUT[RUNNAME.lower()] = D_THISTYPE

        if RUNNAME.lower().startswith(('t1','t2','vasc')):
            DOUT[RUNNAME.lower()] = {}
            D_THISTYPE = {}
            D_THISTYPE['nreps'] = NRUNS

            D_THISTYPE['module_order'] = ["dcm2nii", "spm2_hcorr", "fsl_bet_v5.0.x"]

            DOUT[RUNNAME.lower()] = D_THISTYPE

        if RUNNAME.lower().startswith('dti'):
            DOUT[RUNNAME.lower()] = {}
            D_THISTYPE = {}
            D_THISTYPE['module_order'] = ["recon_multiband"]
            DOUT[RUNNAME.lower()] = D_THISTYPE

        if RUNNAME.lower().startswith('fm_'):
            D_THISTYPE = {}

            DOUT[RUNNAME.lower()] = D_THISTYPE

        if RUNNAME.lower().startswith('spec'):
            D_THISTYPE = {}

            DOUT[RUNNAME.lower()] = D_THISTYPE

# Write out the json
#jfid = open('test_config.json','w')
jfid = open(OUTFILE,'w')
json_data = json.dumps(DOUT, ensure_ascii=False)
python_obj = json.loads(json_data)
jfid.write(json.dumps(python_obj, sort_keys=True, indent=4))
jfid.close()
