# -*- coding: utf-8 -*-
"""
Created on Sat Nov 7 2020

@author: ritesh
"""
import pandas as pd
import numpy as np

df = pd.read_csv('elec-struc_dos_pbe_all.csv')
comp1 = df['Compound']
comp1 = np.array(comp1)
mat = df['Class']
gap = df['Bandgap']

with open('high-thermo_dyn-list.txt','r') as f:
	a = f.readlines()
comp2 = [a[i].split()[0] for i in range(len(a))]

mat_ = []; gap_ = []
for i in range(len(comp1)):
	if str(comp1[i]) in comp2:
		# print(comp1[i])
		# print(mat[i])
		mat_.append(mat[i])
		gap_.append(gap[i])

f.close()

dict = {'Compound': comp2, 'Class': mat_, 'Bandgap': gap_}
df2 = pd.DataFrame(dict, columns=['Compound','Class','Bandgap'])
df2.to_csv('list_high-thermo-dyn.csv', index=False)
