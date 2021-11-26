import os, sys
import numpy as np
import pandas as pd
from pymatgen import Structure
from ase.io import read

f1 = pd.read_csv('form-ener_scan_all.csv')
comp1 = f1['Compound']
form_en1 = f1['H_f']
f2 = pd.read_csv('form-ener_scan_potcar_3.csv')
comp2 = f2['Compound']
form_en2 = f2['H_f']

form_en1c = form_en1.copy()	
for i in range(len(comp2)):
	a = np.where(comp1==comp2[i])
	ind = a[0][0]
	form_en1c[ind] = form_en2[i]

f1['H_f'] = form_en1c
f1.to_csv('form-ener_scan_all_corr.csv', index=False)
f1.to_json('form-ener_scan_all_corr.json')
