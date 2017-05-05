#!/usr/bin/env python

"""Run the script as :"""
"""python eff-mass_calculate.py <coeff. of y^2> <h(for VBM)/e(for CBM)> <x/y>"""

import math as m
import sys
from ase.io import read
from ase import build

structure = read('POSCAR')
array = structure.get_cell_lengths_and_angles()
A = float(sys.argv[1])                                                          #from fitted parabola in xmgrace (through regression)

if sys.argv[3] == 'x':
    a = array[0]
    a *= 10**(-10)                                                              #converting to meter

elif sys.argv[3] == 'y':
    a = array[1]
    a *= 10**(-10)

else:
    print "only x or y direction allowed"

grad_E = 2*A                                                                    #d2E/dk2
grad_E *= 1.6*10**(-19)                                                         #converting eV to J
h_bar = 1.054588664*10**(-34)
c = 2*m.pi/a                                                                    #Conversion factor for k
grad_E /= (c*c)
eff_mass = (h_bar*h_bar)/grad_E
eff_mass /= 9.1*10**(-31)                                                       #Dividing by mass of electron (in kg)

if sys.argv[2] == 'h':
    print "%s(%s) %10.8f" %('hole',sys.argv[3],eff_mass)

elif sys.argv[2] == 'e':
    print "%s(%s) %10.8f" %('electron',sys.argv[3],eff_mass)

else:
    print "Check again, something is wrong..."
