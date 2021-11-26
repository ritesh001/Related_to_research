#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 15:48:57 2020

@author: ritesh
"""

import pandas as pd

df1 = pd.read_csv('hessian-eig_min_all.csv')
df2 = pd.read_csv('elastic-const_all.csv')
df3 = pd.read_csv('thermodynamic-stability_scan_class.csv')

comp = df1['Compound']
hess = df1['Hessian_eig_min_abs']
c11 = df2['C11']
c22 = df2['C22']
c66 = df2['C66']

l = 0; m = 0; h = 0
dyn_list = [0 for i in range(len(comp))]
for i in range(len(comp)):
    if hess[i] >= 2 or c11[i] < 0 or c22[i] < 0 or c66[i] < 0:
        # print(comp[i], hess[i], c11[i], c66[i])
        dyn_list[i] = 'l'
        l += 1
    elif 1e-5 <= hess[i] < 2:
        # print(comp[i], hess[i], c11[i], c66[i])
        dyn_list[i] = 'm'
        m += 1
    elif hess[i] < 1e-5:
        print(comp[i], hess[i], c11[i], c66[i])
        dyn_list[i] = 'h'
        h += 1
        
print(l)
print(m)
print(h)

dict = {'Compound': comp, 'Hessian_eig_min_abs': hess, 'C11': c11, 'C22': c22,
        'C66': c66, 'Dyn_stability_level': dyn_list}
df = pd.DataFrame(dict, columns=['Compound', 'Hessian_eig_min_abs', 'C11', 'C22',
                 'C66', 'Dyn_stability_level'])
df.to_csv('dynamic-stability_class.csv', index=False)