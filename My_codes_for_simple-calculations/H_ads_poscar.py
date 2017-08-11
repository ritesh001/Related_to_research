#!/usr/bin/env python

"""Use this script for adsorbing 1H on the different active sites on structure"""
from ase import Atom, Atoms
from ase import build
from ase.io import read, write
import os
import sys
from shutil import copyfile                                                     # for copying files from one directory to another

curr_dir = os.getcwd()

hetero = read('POSCAR')
hetero.append('H')

for i in range(18):                                                             # no of atoms at which H are to be adsorbed
    j = i+1
    # l = i + 18
    if j < 10:
        k = 'H-0' + str(j)
    else:
        k = 'H-' + str(j)
    path = curr_dir + '/' + k
    os.makedirs(path)
    os.chdir(path)
    pos = hetero.get_positions()
    coor = pos[i][2]
    coor1 = coor + 1.00                                                         # distance at which H is to be adsorbed 
    pos[18] = pos[i]
    pos[18][2] = coor1
    hetero.set_positions(pos)
    write('POSCAR',hetero)
    ## The directory in which this script is run should contain INCAR, KPOINTS and POTCAR ##
    copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
    copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
    copyfile(curr_dir + '/' + 'POTCAR' , path + '/' + 'POTCAR')
    os.chdir(curr_dir)
