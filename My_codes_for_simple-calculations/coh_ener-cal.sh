#!/bin/bash/
for i in Sc Ti V Cr Fe Co Ni Cu Zn
do
cd $i
rm a
tail -1 OSZICAR | awk '{printf"%15.12f\n",$5}' >> p
tail -1 ../../../relax/OSZICAR | awk '{printf"%15.12f\n",$5}' >> p
tail -1 ../../../../coh_ener_TM/$i/OSZICAR | awk '{printf"%15.12f\n",$5}' >> p
cat >form_ener.py <<!
f=open("p","r")
b=[]
for line in f:
    a=line.split()
    a=float(a[0])
    b.append(a)
c=b[2]/2
print(b[0]-b[1]-c)
!
echo $i >> ../a	
python form_ener.py >> ../a
cd ../
done
paste -d " "  - - < a >> coh_ener
