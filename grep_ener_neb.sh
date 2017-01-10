#!/bin/bash/
for i in 00 01 02 03 04 05 
do 
tail -1 $i/OSZICAR | awk '{printf"%15.12f\n",$5}' >> energies
done
