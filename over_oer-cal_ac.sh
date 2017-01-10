#!/bin/bash/
for i in Sc Ti V Cr Mn Fe Co Ni Cu Zn
do
cd $i
rm over-cal_oer_ac.py
awk 'FNR<10 {print $1}' G-cal.py > over-cal_oer_ac.py
cat >> over-cal_oer_ac.py <<!
U = 0.402
pH = 10

#Calculation of free energies

#G1 = 0.0
#print(G1)

G1 = mew_oh - mew_pris - mew_h2o + 0.5*mew_h2 - 0.06*pH - 1*U
#print(G1)

G2 = mew_oh - mew_o - 0.5*mew_h2 + 2*U +0.06*pH
G2 = -G2
#print(G2)

G3 = mew_o - mew_ooh + mew_h2o - 0.5*mew_h2 + 3*U + 0.06*pH
G3 = -G3
#print(G3)

G4 = 4*0.402 - 4*U
#print(G4)

G = [G1,G2,G3,G4]
a = max(G)
b = G.index(a)
over = G[b] - G[b-1]
print("{:5} {:5.3f}".format("$i",over))
!
python3 over-cal_oer_ac.py >> ../results/G-TM_ac/OER/overpot
cd ../
done 
