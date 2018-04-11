#!/usr/bin/env python

from sys import argv
import json

DATFILE=argv[1]

jfid = open('rawdata.json','w')
d = {}
d['func'] = {}
d['anat'] = {}
d['spectro'] = {}
d['dti'] = {}
d['dti_fieldmap'] = {}
d['func_fieldmap'] = {}

# need also func dicom field maps

with open(DATFILE,'r') as fid:
    #for line in sorted(fid,key=lambda x: int(x[5])):
    for line in sorted(fid,key=lambda line: line.split()[4]):
        lst = line.strip().split(' ')
        RAW = lst[0]
        SUBJ = lst[1]
        SENUM = '{:02d}'.format(int(lst[2]))
        SEDESC = lst[3]
        DATETIME = lst[4]
        PHYS = lst[5:9]

        d['subject'] = SUBJ

        if SEDESC.lower().startswith('func'):
            SETYPE = 'func'
            if RAW.lower().endswith('.data'):
                ACQTYPE = 'multiband'
            elif RAW.lower().startswith('s0'):
                ACQTYPE = 'epi'
            elif RAW.lower().endswith('.7'):
                ACQTYPE = 'spiral'

                # Need to account for same series number for a task
                LSERIES = []
                for kn in d['func'].keys():
                    if kn.startswith(SENUM):
                        LSERIES.append(kn)

                NTHISSERIESNUMEXISTING = len(LSERIES)
                THISNUM = len(LSERIES) + 1
                SENUM = '{}_{:02d}'.format(SENUM,THISNUM)



            d['func'][SENUM] = {}
            d['func'][SENUM]['rawdata'] = RAW;
            d['func'][SENUM]['acqtype'] = ACQTYPE;
            d['func'][SENUM]['sedesc'] = SEDESC;
            d['func'][SENUM]['phys_files'] = PHYS

        elif SEDESC.lower().startswith('dti'):
            SETYPE = 'dti'
            if RAW.lower().endswith('.data'):
                ACQTYPE = 'multiband'
            elif RAW.lower().startswith('s0'):
                ACQTYPE = 'epi'

            d['dti'][SENUM] = {}
            d['dti'][SENUM]['rawdata'] = RAW
            d['dti'][SENUM]['acqtype'] = ACQTYPE
            d['dti'][SENUM]['sedesc'] = SEDESC

        elif SEDESC.lower().startswith('fm_dti'):
            SETYPE = 'dti_fieldmap'
            d['dti_fieldmap'][SENUM] = {}
            d['dti_fieldmap'][SENUM]['rawdata'] = RAW
            d['dti_fieldmap'][SENUM]['sedesc'] = SEDESC

        elif SEDESC.lower().startswith('fm') and not SEDESC.lower().startswith('fm_dti'):
            SETYPE = 'func_fieldmap'
            d['func_fieldmap'][SENUM] = {}
            d['func_fieldmap'][SENUM]['rawdata'] = RAW
            d['func_fieldmap'][SENUM]['sedesc'] = SEDESC

        elif SEDESC.lower().startswith('t1') or SEDESC.lower().startswith('t2') or SEDESC.lower().startswith('vasc'):
            SETYPE = 'anat'

            d['anat'][SENUM] = {}
            d['anat'][SENUM]['rawdata'] = RAW
            d['anat'][SENUM]['sedesc'] = SEDESC

        elif SEDESC.lower().startswith('spect'):
            SETYPE = 'spectro'
            d['spectro'][SENUM] = {}
            d['spectro'][SENUM]['rawdata'] = RAW
            d['spectro'][SENUM]['sedesc'] = SEDESC

json_data = json.dumps(d, ensure_ascii=False)
python_obj = json.loads(json_data)
jfid.write(json.dumps(python_obj, sort_keys=True, indent=4))
jfid.close()
