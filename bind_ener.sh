#!/bin/bash/
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13
do
cd $i
echo $i > a
tail -1 ads_o2/OSZICAR | awk '{printf"%15.12f\n",$5}' > b 
tail -1 relax/OSZICAR | awk '{printf"%15.12f\n",$5}' > c
tail -1 ../OSZICAR_o2 | awk '{printf"%15.12f\n",$5}' > d
cat a b c d >> ../ads_ener
rm {a,b,c,d}
cd ../
done
