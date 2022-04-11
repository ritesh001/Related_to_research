#!/usr/bin/env python

"""Use it for generating kpoints along special k-path; may be required in HSE calculation"""
"""Use it as python special_k_path_vasp.py <grid>"""

import sys
f1 = open('KPOINTS','r')
b = []
for line in f1:
	a = line.split()
	a = [a[i] for i in range(len(a))]
	b.append(a)

f2 = open('kpts','w')
g = int(sys.argv[1]) - 1
m = float(g)
for j in range(4,len(b),3):
	dx = float((float(b[j+1][0]) - float(b[j][0]))/m); dy = float((float(b[j+1][1]) - float(b[j][1]))/m); dz = float((float(b[j+1][2]) - float(b[j][2]))/m)
	for k in range(g+1):
		kx = float(b[j][0]) + (dx * k); ky = float(b[j][1]) + (dy * k); kz = float(b[j][2]) + (dz * k)
		# print "%5.3f %5.3f %5.3f" %(kx, ky, kz)
		f2.write("%9.6f %9.6f %9.6f %4.1f\n" %(kx, ky, kz, 0))

f1.close(); f2.close()