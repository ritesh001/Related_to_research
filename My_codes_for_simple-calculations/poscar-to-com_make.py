### First you need to convert POSCAR/CONTCAR from direct to cartesian coordinates ###

import math as m
print("%chk=C:\Users\deya\Desktop\H3BNH3.chk")
print("#pbepbe/3-21g/auto")
print("")
print("Title Card Required")
print("")
print("0 1")
f=open("CONTCAR","r")
b=[]
for line in f:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
#print(b)
for i in range(8,68):                                                                                  # for C coordinates
     print(" C{:30.10f} {:15.10f} {:15.10f}".format(float(b[i][0]),float(b[i][1]),float(b[i][2])))

for i in range(68,110):                                                                                # for N coordinates
     print(" N{:30.10f} {:15.10f} {:15.10f}".format(float(b[i][0]),float(b[i][1]),float(b[i][2])))

print(" H{:30.10f} {:15.10f} {:15.10f}".format(float(b[110][0]),float(b[110][1]),float(b[110][2])))    # for H coordinates

for i in range(2,5):                                                                                   # Translation vector
     print(" Tv{:30.10f} {:15.10f} {:15.10f}".format(float(b[i][0]),float(b[i][1]),float(b[i][2])))
