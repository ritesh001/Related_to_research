#!/usr/bin/env python

"""Run the vbm-cbm.sh script from directory where data is to be stored"""
"""Directories where uniaxial strain are run, are named as us<strain in % with + or ->"""
"""In these directories, bandstructures are run with another directory named as PBE_bands"""

import os, os.path
cur_path = os.getcwd()                                                          # current directory
pre_path = os.path.abspath(os.path.join(cur_path,os.pardir))                    # previous directory
pre_pre_path = os.path.abspath(os.path.join(pre_path,os.pardir))                # previous to previous directory
file1 = 'VBM.dat'; file2 = 'CBM.dat'
fullpath1 = pre_pre_path + '/' + file1; fullpath2 = pre_pre_path + '/' + file2

"""output of bandgap.pl stored into abc file"""
f = open('abc','r')
f1 = open(fullpath1,'a'); f2 = open(fullpath2,'a')
str1 = cur_path.split('/')
a = str1[len(str1)-2]
str3 = a.split('s')
e = float(str3[1])/100

b = []
for line in f:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
f.close()

c = [float(b[11][3]),float(b[11][4]),float(b[11][5])]                           # vbm energy
d = [float(b[14][3]),float(b[14][4]),float(b[14][5])]                           # cbm energy

"""Change the value of vaccum level accordingly"""
vaccum_level = 2.96                                                             # need to enter manually from LOCPOT file
vbm = float(b[10][7]) - vaccum_level; cbm = float(b[13][7]) - vaccum_level
f1.write("%6.3f %6.4f\n" %(e, vbm)); f2.write("%6.3f %6.4f\n" %(e, cbm))
f.close()
f1.close(); f2.close()
