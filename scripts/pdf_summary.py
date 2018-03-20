#!/usr/bin/env python

from sys import argv
import os
import subprocess
import datetime
import socket

def txt2pdf(FILE):
    BASE = os.path.splitext(FILE)[0] 

    # Make a ps
    CMD_ES = 'enscript -r -p {} {} -f Courier16 &> /dev/null'.format(BASE+'.ps', FILE)
    subprocess.call(CMD_ES,shell=True)

    # Now convert to a pdf
    CMD_PDF = 'ps2pdf {} {} &> /dev/null'.format(BASE+'.ps', BASE+'.pdf')
    subprocess.call(CMD_PDF,shell=True)

    # Remove temp txt + ps files.
    os.remove(BASE+'.ps')
    os.remove(FILE)

def bundle():
    CMD_FIND = "find ./ -name '*.pdf' | xargs ls -rt > pdf_lst"
    subprocess.call(CMD_FIND,shell=True)

    f = open('pdf_lst','r')
    l = f.readlines()
    SFILES = ' '.join(l).replace('\n',' ')
    CMD_PDF = "gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=preproc.pdf {} 2>/dev/null".format(SFILES)
    subprocess.call(CMD_PDF,shell=True)
	#rm -f PDF_LIST


def series_header(FILENAME,TEXT):
    f = open(FILENAME+'.txt','w')
    f.write(TEXT)
    f.close()
    print(FILENAME+'.txt')

    txt2pdf(FILENAME+'.txt')

def header():
    DATE = datetime.datetime.now()
    f = open('preproc_header.txt','w')
    f.write('Date: {}'.format(DATE))
    f.write('\nHost: {}'.format(socket.gethostname()))
    f.write('\nDir: {}'.format(os.getcwd()))
    f.close()

    txt2pdf('preproc_header.txt')
