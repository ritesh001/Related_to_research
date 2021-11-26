# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 00:17:42 2020

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from pymatgen import Structure
from pymatgen.io.cif import CifWriter
#from ase.io import read
import os
import numpy as np

data_or = pd.read_csv('form-ener_scan_30-06-20.csv')     ## change the file name here
comp = data_or['Compound']
images = []
curr_dir = os.getcwd()

dict = {'Compound':comp}
df = pd.DataFrame(dict)

comp_id = []
comp_arr = np.array(comp)
df_all = pd.read_json('all-list_comp.json')
for i in range(len(df_all['Compound'])):
    if df_all['Compound'][i] in comp_arr:
       #print(df_all['Compound_id'][i])
       comp_id.append(df_all['Compound_id'][i])

cif_dir = '/home/mrcuser/Ritesh/cifs-for-cgcnn'
for i in range(len(comp_id)):
    print(comp[i])
    path = curr_dir + '/' + comp[i]
    os.chdir(path)
    struc = Structure.from_file('POSCAR')
    w = CifWriter(struc, symprec=0.1)
    fil = str(comp_id[i]) + '.cif'
    os.chdir(cif_dir)
    w.write_file(fil)
    #images.append(struc)
    os.chdir(curr_dir)

#df.drop(['structure', 'Composition', 'compound possible'], axis=1, inplace=True)
df['Compound_id'] = comp_id
df['Formation_energy'] = data_or['H_f']
df.to_csv('id_prop.csv', index=False)
df_label = df.columns
l = len(df_label)
print(l)
