#!/usr/bin/env python

"""Use this script for adsorbing 1H2O on the different active sites on structure"""
from ase import Atom, Atoms
from ase.io import read, write
import os
import sys
from shutil import copyfile                                                     # for copying files from one directory to another
from ase.visualize import view

curr_dir = os.getcwd()

hetero = read('POSCAR')
n = hetero.get_number_of_atoms()
hetero.append('O'); hetero.append('H'); hetero.append('H')

for i in range(14,21):                                                           # no of atoms at which H2O are to be adsorbed
    j = i+1
    # l = i + 18
    if j < 10:
        k = 'H2O-0' + str(j)
    else:
        k = 'H2O-' + str(j)
    path = curr_dir + '/' + k
    os.makedirs(path)
    os.chdir(path)
    pos = hetero.get_positions()
    coor = pos[i][2]
    coor1 = coor + 3.0                                                         # distance at which O is to be adsorbed, '+' for upside and '-' for downside
    pos[n][0] = pos[i][0]; pos[n][1] = pos[i][1]; pos[n][2] = coor1 # coordinates of O
    pos[n+1][0] = pos[n][0] - 0.783975893; pos[n+1][1] = pos[n][1]; pos[n+1][2] = pos[n][2] + 0.554059382                        # coordinates of H1
    pos[n+2][0] = pos[n][0] + 0.783975893; pos[n+2][1] = pos[n][1]; pos[n+2][2] = pos[n][2] + 0.554059382                        # coordinates of H2
    hetero.set_positions(pos)
    write('POSCAR',hetero)
    ## The directory in which this script is run should contain INCAR, KPOINTS and POTCAR ##
    copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
    copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
    copyfile(curr_dir + '/' + 'POTCAR' , path + '/' + 'POTCAR')
    os.chdir(curr_dir)
