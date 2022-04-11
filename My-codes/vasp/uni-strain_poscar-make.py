#!/usr/bin/env python

"""Run the script as :"""
"""python uni-strain_poscar-make.py <x/y>"""

import os
import sys
from ase.io import read, write
from ase import Atom, Atoms
path = os.getcwd()
f = open('a_values','w')

b = sys.argv[1]

j = -7                                                                          #initial strain
for i in range(8):                                                              #no of poscars to generate
	poscar = read('POSCAR')
	a = poscar.cell
	k =  j + i*2.0                                                              #interval of strains
	l = k/100
	if k > 0:
		c = '+' + str(k)
	else:
		c = str(k)
	path1 = path + '/' + 'us' + c + '/' + 'relax'                               #make the folders in this way
	# os.mkdir(path1)
	os.chdir(path1)
	if b == 'x':
		m = a[0][0] * l + a[0][0]
		poscar.cell[0][0] = m
	elif b == 'y':
		m = a[1][1] * l + a[1][1]
		poscar.cell[1][1] = m
	else :
		print 'Only x or y allowed ...'

	write('POSCAR',poscar)
	os.chdir(path)
	f.write("%12.8f %12.8f\n" %(k, m))

f.close()
