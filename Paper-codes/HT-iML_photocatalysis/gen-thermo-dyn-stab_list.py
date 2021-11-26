#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:17:33 2020

@author: ritesh
"""

import pandas as pd

df1 = pd.read_csv('thermodynamic-stability_scan_class.csv')
df2 = pd.read_csv('dynamic-stability_class.csv')
df3 = pd.read_csv('hessian-eig_min_all.csv')
df4 = pd.read_csv('elastic-const_all.csv')

comp = df1['Compound']
thermo_list = df1['Thermo_stability_level']
dyn_list = df2['Dyn_stability_level']

hess = df3['Hessian_eig_min_abs']
c11 = df4['C11']
c22 = df4['C22']
c66 = df4['C66']
form_en = df1['Formation_energy']
e_hull = df1['E_above_hull']

tot_list = []
for i in range(len(comp)):
    tot_list.append(thermo_list[i] + dyn_list[i])

print(tot_list.count('Hh'))
    
dict = {'Compound': comp, 'Formation_energy': form_en, 'E_above_hull':e_hull, 
        'Thermo_stability_level': thermo_list, 'C11': c11, 'C22': c22, 'C66': c66,
        'Hessian_eig_min_abs':hess, 'Dyn_stability_level': dyn_list, 'Thermo_Dyn_stability_level': tot_list}
df = pd.DataFrame(dict, columns=['Compound', 'Formation_energy', 'E_above_hull', 
                                 'Hessian_eig_min_abs', 'C11', 'C22', 'C66', 'Thermo_stability_level',
                                 'Dyn_stability_level', 'Thermo_Dyn_stability_level'])
df.to_csv('thermo_dynamic-stability_class.csv', index=False)