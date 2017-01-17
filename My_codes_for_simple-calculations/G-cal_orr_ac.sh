#!/bin/bash/
for i in Sc Ti V Cr Mn Fe Co Ni Cu Zn
do
cd $i
rm G-cal_orr_ac.py
awk 'FNR<10 {print $1}' G-cal.py > G-cal_orr_ac.py
cat >> G-cal_orr_ac.py <<!
U = 0.402
pH = 10

#Calculation of free energies

G1 = 0.0
print(G1)

G2 = mew_ooh - mew_o2 - 0.5*mew_h2 + 1*U + 0.06*pH 
print(G2)

G3 = mew_o - mew_ooh + mew_h2o - 0.5*mew_h2 + 2*U + 0.06*pH
print(G3)

G4 = mew_oh - mew_o - 0.5*mew_h2 + 3*U +0.06*pH
print(G4)

G5 = -1.608 + 4*U
print(G5)
!
python G-cal_orr_ac.py > ../results/G-TM_ac/ORR/U_0.402/G_$i
cd ../
done
