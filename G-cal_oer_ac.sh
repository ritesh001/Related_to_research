#!/bin/bash/
for i in Sc Ti V Cr Mn Fe Co Ni Cu Zn
do
cd $i
rm G-cal_oer_ac.py
awk 'FNR<10 {print $1}' G-cal.py > G-cal_oer_ac.py
cat >> G-cal_oer_ac.py <<!
U = 0.402
pH = 10

#Calculation of free energies

G1 = 0.0
print(G1)

G2 = mew_oh - mew_pris - mew_h2o + 0.5*mew_h2 - 0.06*pH - 1*U
print(G2)

G3 = mew_oh - mew_o - 0.5*mew_h2 + 2*U +0.06*pH
G3 = -G3
print(G3)

G4 = mew_o - mew_ooh + mew_h2o - 0.5*mew_h2 + 3*U + 0.06*pH
G4 = -G4
print(G4)

G5 = 4*0.402 - 4*U
print(G5)
!
python G-cal_oer_ac.py > ../results/G-TM_ac/OER/U_0.402/G_$i
cd ../
done
