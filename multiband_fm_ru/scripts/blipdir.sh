#!/bin/bash

PFILE=$(ls P*7)

BLIPDIR=$(python <<EOF
import struct
f = open('${PFILE}','r')
f.seek(147732)
blipvar = struct.unpack('f', f.read(4))[0]
if blipvar == 1:
	BLIPDIR = -1
else:
	BLIPDIR = +1
f.close()
print(BLIPDIR)
EOF
)

echo $BLIPDIR