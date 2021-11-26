#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from ase.io import read
import os

curr_dir = os.getcwd()
list = pd.read_csv('all-list_comp.csv')
#list = pd.read_csv('list_comp.csv')
a = list['Compound']

comp = []; eig_hess = []
for i in range(len(a)):
	path = curr_dir + '/' + a[i]
	comp.append(a[i])        ## uncomment when list contains '/' at the end
	os.chdir(path)
	print(path)
	struc = read('POSCAR')
	#n = struc.get_global_number_of_atoms()
	n = struc.get_number_of_atoms()
	n_mode = 3 * n

	out = open('OUTCAR', 'r')
	searchlines = out.readlines()
	out.close()
	for i, line in enumerate(searchlines):
	        if "SECOND DERIVATIVES" in line:
	            s = i

	m = [[0 for j in range(n_mode)] for i in range(n_mode)]

	for i in range(n_mode):
	    for j in range(n_mode):
	        m[i][j] = float(searchlines[s+i+3].split()[j+1])

	m = np.array(m)
	sym_m = 0.5 * (m + m.transpose())          ## Hessian matrix --> a symmetric matrix
	w, v = np.linalg.eig(sym_m)

	# print(min(w))
	# print(min(abs(w)))
	eig_hess.append(min(abs(w)))
	os.chdir(curr_dir)

dict = {'Compound': comp, 'Hessian_eig_min_abs': eig_hess}
df = pd.DataFrame(dict, columns=['Compound', 'Hessian_eig_min_abs'])
file_name_csv = 'hessian-eig_min_all'  + '.csv'
file_name_json = 'hessian-eig_min_all'  + '.json'
df.to_csv(file_name_csv, index=False)
df.to_json(file_name_json)
