### First you need to place all cordinates in one sequence as given in line 9 ###

import math as m
print("System = Co6Nb_H2O")
print("{:12.10f}".format(1))
print("{:15.10f} {:15.10f} {:15.10f}".format(15,0,0))
print("{:15.10f} {:15.10f} {:15.10f}".format(0,15,0))
print("{:15.10f} {:15.10f} {:15.10f}".format(0,0,15))
print("Co","Nb","H","N","B","O")
print(6,1,8,1,1,1)
print("Cartesian")
f=open("H2O-5.com","r")
b=[]
for line in f:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
#print(b)
for i in range(6,(len(b)-4)):
     print("{:15.10f} {:15.10f} {:15.10f}".format(float(b[i][1]),float(b[i][2]),float(b[i][3])))
#print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
#print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
#print("{:15.10f} {:15.10f} {:15.10f}".format(x,y,z))
#print("{:15.10f} {:15.10f} {:15.10f}".format(7.5,7.5,5.0))

