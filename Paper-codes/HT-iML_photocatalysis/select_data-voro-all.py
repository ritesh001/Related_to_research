# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 07:10:30 2020

@author: ritesh
"""

import pandas as pd
import numpy as np

orig_data1 = pd.read_excel('formation_energy_scan-calculate_all.xls', sheet_name='M_III_X-Y')
orig_data2 = pd.read_excel('formation_energy_scan-calculate_all.xls', sheet_name='M_II_X-Y')
comp_data1 = orig_data1.iloc[:,0]; comp_data2 = orig_data2.iloc[:,0]
e_f1 = orig_data1.iloc[:,5]; e_f2 = orig_data2.iloc[:,5]

voro_data = pd.read_csv('data_voro.csv')
comp_voro = voro_data['Compound']
e_fv = [0 for i in range(len(comp_voro))]
#ind1 = np.isin(comp_data1, comp_voro)

for i in range(len(comp_voro)):
	for j in range(len(comp_data1)):
		if comp_voro[i] == comp_data1[j]:
			print(comp_data1[j])
			e_fv[i] = e_f1[j]
			
for i in range(len(comp_voro)):
	for j in range(len(comp_data2)):
		if comp_voro[i] == comp_data2[j]:
			print(comp_data2[j])
			e_fv[i] = e_f2[j]

voro_data['formation_energy'] = e_fv
df = voro_data.copy()
ind = []
for i in range(len(e_fv)):
	if e_fv[i] == 0:
		ind.append(i)
	elif e_fv[i] == 'nan':
		ind.append(i)

df.drop(ind, inplace=True)
df.to_csv('fin_voro_data.csv', index=False)
