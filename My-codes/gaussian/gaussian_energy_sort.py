#!/usr/bin/env python
"""Use it for moving top stable structures from CK run to"""
"""another folder named 'level_2'"""

import numpy as np
import os
from shutil import copyfile

f = np.genfromtxt('energies.dat', delimiter='', dtype=None, names=('structure', 'energy')) # to read a file containing both string and float
f_sorted = sorted(f, key=lambda x:x[1])                                         # to sort an array based on one column

f2 = 'energies_sorted.dat'
with open(f2, 'w') as f_obj:
    for i in range(len(f_sorted)):
        f_obj.write('%16s %16.8f\n' %(f_sorted[i][0], f_sorted[i][1]))

curr_dir = os.getcwd()
next_dir = curr_dir + '/../' + 'level_2'

for i in range(30):
    copyfile(curr_dir + '/' + f_sorted[i][0] , next_dir + '/' + f_sorted[i][0])
