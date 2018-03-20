#!/usr/bin/python

# Quick script to use dicom module to read dcm header
# $Id: dcmheader.py 1418 2014-05-19 13:24:54Z klitinas $

import sys

try:
  import dicom
except:
  import pydicom as dicom

strFile = sys.argv[1]

ds = dicom.read_file(strFile)
print ds
