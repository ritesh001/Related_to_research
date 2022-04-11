#!/bin/bash/
for i in Sc Ti V Cr Mn Fe Co Ni Cu Zn
do
cd $i
rm over-cal.py
awk 'FNR<9 {print $1}' G-cal_1.py > over-cal.py
cat >> over-cal.py <<!
# Calculation of free energies

G1 = mew_o2 - 4.92 - 2*mew_h2o + 2*mew_h2 - mew_pris
#print(G1-G1)

G2 = mew_ooh - mew_o2 - 0.5*mew_h2 + 1.57 - G1
#print(G2)

G3 = mew_o - mew_ooh + mew_h2o - 0.5*mew_h2 + 1.57 - G1
#print(G3)

G4 = mew_oh - mew_o - 0.5*mew_h2 + 1.57 - G1
#print(G4)

G5 = mew_pris - mew_oh + mew_h2o - 0.5*mew_h2 + 1.57 - G1
#print(G5)

#Calculation of overpotential

G = [G2,G3,G4,G5]
G_ORR = min(G)
eta_ORR = abs(G_ORR) - 0.401
print("{:5} {:6.3f}".format("Sc",eta_ORR))
!
python3 over-cal.py >> ../results/G-TM/overpot
cd ../
done
