# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:30:02 2020

@author: ritesh
"""

import numpy as np
import pandas as pd

df = pd.read_csv('thermodynamic-stability_scan_reg.csv')
e_form = df['Formation_energy']
e_hull = df['E_above_hull']
comp = df['Compound']

thermo_level = [0 for i in range(len(comp))]
h = 0; m = 0; l = 0
for j in range(len(comp)):
    print(comp[j])
    s = e_hull[j] + 0.2
    #print(e_hull[j])
    #if e_form[j] < s:               ## since pymatgen dmes not support > 4-component convex hull figures
    if e_hull[j] < 0.2:               ## since pymatgen dmes not support > 4-component convex hull figures
       thermo_level[j] = 'H'
       h += 1
    elif e_form[j] < 0.2: 
       thermo_level[j] = 'M'
       m += 1
    elif e_form[j] > 0.2: 
       thermo_level[j] = 'L'
       l += 1

print(h, m, l)
dict = {'Compound': comp, 'Formation_energy': e_form, 'E_above_hull': e_hull, 'Thermo_stability_level': thermo_level}
df2 = pd.DataFrame(dict, columns=['Compound', 'Formation_energy', 'E_above_hull', 'Thermo_stability_level'])
df2.to_csv('thermodynamic-stability_scan_class.csv', index=False)
