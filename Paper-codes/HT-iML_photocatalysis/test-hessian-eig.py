#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from ase.io import read

struc = read('POSCAR')
n = struc.get_global_number_of_atoms()
n_mode = 3 * n

out = open('OUTCAR', 'r')
searchlines = out.readlines()
out.close()
for i, line in enumerate(searchlines):
        if "SECOND DERIVATIVES" in line:
#             print(line)
            s = i

#for i in range(n_mode):
#    print(searchlines[s+i+3])

searchlines[s+3].split()
m = [[0 for j in range(n_mode)] for i in range(n_mode)]

for i in range(n_mode):
    for j in range(n_mode):
        m[i][j] = float(searchlines[s+i+3].split()[j+1])

m = np.array(m)
sym_m = 0.5 * (m + m.transpose())          ## Hessian matrix --> a symmetric matrix

sym_m.transpose()
w, v = np.linalg.eig(sym_m)

print(min(w))
print(min(abs(w)))
