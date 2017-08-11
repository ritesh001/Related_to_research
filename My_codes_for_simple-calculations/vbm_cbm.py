#!/usr/bin/env python
"""Use it for finding vbm and cbm energies and also their corresponding k-points"""
"""Run it as :"""
"""python vbm_cbm.py <no of bands> <valence band no>"""

import sys
import numpy as np

f = open('eig','r')

b = []

for line in f:
    a = line.split()
    a = [float(a[i]) for i in range(len(a))]
    b.append(a)
# print b

f1 = open('vb-energy.dat', 'w')
f2 = open('cb-energy.dat', 'w')

length = int(sys.argv[1]) + 2
v = int(sys.argv[2]); c = v + 1
for i in range(0,len(b),length):                                                # length = periodicity in 'eig' file
    j = i + v                                                                   # v = valence band no., check from OUTCAR
    k = i + c                                                                   # c = conduction band no., check from OUTCAR
    e_v = b[j][1]
    e_c = b[k][1]
    f1.write('%10.6f %10.6f %10.6f %10.6f\n' %(b[i][0], b[i][1], b[i][2], e_v))
    f2.write('%10.6f %10.6f %10.6f %10.6f\n' %(b[i][0], b[i][1], b[i][2], e_c))
f1.close()
f2.close()

## vbm and cbm ##
vbm = np.loadtxt('vb-energy.dat', usecols=[3]).max()                      # for finding the max value of 4th column of file
cbm = np.loadtxt('cb-energy.dat', usecols=[3]).min()                      # for finding the min value of 4th column of file
## index of vbm and cbm ##
vbm_index = np.loadtxt('vb-energy.dat', usecols=[3]).argmax()                   # for finding the indices of max value of 4th column of file
cbm_index = np.loadtxt('cb-energy.dat', usecols=[3]).argmin()                   # for finding the indices of min value of 4th column of file
## creating arrays for k-points ##
vb = np.loadtxt('vb-energy.dat', usecols=[0,1,2])                               # for creating an array from 1st, 2nd & 3rd columns of file
cb = np.loadtxt('cb-energy.dat', usecols=[0,1,2])                               # for creating an array from 1st, 2nd & 3rd columns of file

print 'VBM = %f at %r' %(vbm, vb[vbm_index])
print 'CBM = %f at %r' %(cbm, cb[cbm_index])
