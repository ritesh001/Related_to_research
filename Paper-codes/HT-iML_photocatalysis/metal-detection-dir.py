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

for i in range(len(x)):
    path1 = pwd + '/' + x[i]
    os.chdir(path1)
    f = open('metals.dat','w')
    for j in range(len(m)):
        path2 = path1 + '/' + m[j] + '/' + 'scan'
        os.chdir(path2)
        dosrun = Vasprun("./vasprun.xml")
        a = dosrun.get_band_structure()
        if a.is_metal() == True:
            os.chdir(path1)
            f.write('%s \n' %(m[j]))
        else:
            continue
    f.close()

os.chdir(pwd)