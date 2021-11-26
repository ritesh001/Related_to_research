#!/usr/bin/env python

"""Run the script as :"""
"""python carrier_mobility.py <'e' or 'h'>"""
"""Also requires slope.dat and eff-mass.dat in required format"""

import sys
import numpy as np
from ase.io import read
from ase import build

structure = read('POSCAR')
array = structure.get_cell_lengths_and_angles()

##Reading slope.dat##
f1 = open('slope.dat','r')
b = []
for line in f1:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
f1.close()

##Reading eff-mass.dat##
f2 = open('eff-mass.dat','r')
d = []
for line in f2:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    d.append(a)
f2.close()

if sys.argv[1] == 'h':
    deform = float(b[1][2])
    eff = float(d[0][1])
    eff *= float(d[1][1])
elif sys.argv[1] == 'e':
    deform = float(b[2][2])
    eff = float(d[2][1])
    eff *= float(d[3][1])

A = array[0]*array[1]
A *= (1e-10*1e-10)
# mod = 2 * float(sys.argv[1])
mod = 2 * float(b[5][2])
c = 1.60217662e-19
mod *= c                                                                        # in units of J
mod /= A
print "Elastic modulus = %f N m^-1" %mod
k_B = 1.38064852e-23
T = 298
e = 1.60217662e-19
h = 6.626e-34
h_bar = h/(2*np.pi)

eff *= 9.10938356e-31 * 9.10938356e-31
deform *= c                                                                     # in units of J

mew = (2 * e * (h_bar**3) * mod) / (3 * k_B * T * (eff) * (deform**2))          # in m^2 V^-1 s^-1
mew *= 1e4                                                                      # convert m^2 into cm^2

print "Mobility = %f cm^2 V^-1 s^-1" %(mew)
