### First run bader script from which ACF.dat file is generated ###

import os

f0 = open("POSCAR","r")
f01 = open("POTCAR","r")
f1 = open("ACF.dat","r")
f2 = open("charges_on_atoms","w")
#f3 = open("min-max_charges","w")
f4 = open("test","w")
b=[]; b1=[]
valence = []

sum_C = 0
sum_N = 0
sum_W = 0
sum_S = 0

C_charges=[]
N_charges=[]
W_charges=[]
S_charges=[]

##Reading POSCAR file##
for line in f0:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
f0.close()

#print(b[5][1],len(b[5]))
atoms = []
atoms_number = []
for j in range(len(b[5])):
    atoms.append(b[5][j])
    atoms_number.append(int(b[6][j]))
#print atoms, atoms_number
atoms_p = [('=' + atoms[i]) for i in range(len(atoms))]
#print atoms_p

##Reading POTCAR file##
searchlines = f01.readlines()
f01.close()
for i, line in enumerate(searchlines):
    for j in range(len(atoms_p)):
        if atoms_p[j] in line:
            for l in searchlines[i-2]:
                f4.write(l,)
f4.close()

f5 = open("test","r")
for line in f5:
    a0 = line.split()
    a0 = [float(a0[i]) for i in range(len(a0))]
    valence.append(a0)
f5.close()
#print valence[2][0]

os.remove("test")

##Reading ACF.dat file##
for line in f1:
    a1 = line.split()
    a1 = [a1[i] for i in range(len(a1))]
    b1.append(a1)
#print(b1)

s = 0
for i in range(len(atoms)):
    for j in range(atoms_number[i]):
        #print j
        k = j + s
        charge = valence[i][0] - float(b1[k+2][4])
        #print charge
        f2.write("%4d %s%d %12.8f\n" % ((k+1),atoms[i],(j+1),charge))
    #print j
    s = s + j + 1

f1.close()
f2.close()
#f3.close()
