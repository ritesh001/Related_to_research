#!/bin/bash/
for i in Sc Ti V Cr Mn Fe Co Ni Cu Zn
do
cd $i
cd ads_o2
cd vib_freq
cp ../../../ZPE-TS_cal.py .
tail -1 OSZICAR | awk '{printf"%15.12f\n",$5}' >> ../a
grep THz OUTCAR | awk '{printf"%15.12f",($10*1E-3)/2}' > b
python ZPE-TS_cal.py >> ../a
cd ../
awk '{ sum += $1 } END { print sum }' a > ../mew_o2
cd ../../
done
