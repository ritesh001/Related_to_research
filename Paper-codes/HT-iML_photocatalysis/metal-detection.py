#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:29:20 2018

@author: ritesh
"""

from warnings import filterwarnings
filterwarnings("ignore")
from pymatgen.io.vasp import Vasprun
import os
pwd = os.getcwd()
x = ['Br','Cl','CN','F','I','NC','NCO','NCS','NO','OCN','SCN','SH']
m = ['Ba','Be','Ca','Cd','Co','Cu','Fe','Mg','Mn','Ni','Pb','Pd','Pt','Sr','Zn']

f = open('non-metals.dat','w')
for i in range(len(x)):
    for j in range(len(m)):
        path = pwd + '/' + x[i] + '/' + m[j] + '/' + 'scan'
        os.chdir(path)
        dosrun = Vasprun("./vasprun.xml")
        a = dosrun.get_band_structure()
        if a.is_metal() == False:
            os.chdir(pwd)
            f.write('%s/%s \n' %(x[i],m[j]))
        else:
            continue

os.chdir(pwd)
f.close()