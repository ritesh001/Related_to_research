#!/bin/bash/

cd vib_freq
cp ../ZPE-TS_cal.py .
grep THz OUTCAR | awk '{printf"%15.12f",($10*1E-3)/2}' > c
python ZPE-TS_cal.py >> ../G_H.dat
rm {ZPE-TS_cal.py,c}
cd ../
awk '{ sum += $1 } END { print sum }' G_H.dat >> G_H.dat
