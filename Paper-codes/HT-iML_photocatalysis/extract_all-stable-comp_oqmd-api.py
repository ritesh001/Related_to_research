# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 23:05:33 2020

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
import qmpy_rester as qr
# from qmpy import io
import pandas as pd
from ase.spacegroup import crystal as crys
from ase.io import read, write
from ase import Atoms
import os
from pymatgen import Structure
from pymatgen.io.vasp.sets import MPRelaxSet

all_list = pd.read_json('all-list_comp.json')
all_list_comp = all_list['Compound']
all_list_elem = all_list['Elements']

def extract_elem(arr):
    elem = ''
    for i in range(len(arr)):
        elem += arr[i]
        if i == len(arr)-1:
           continue
        else:
           elem += str('-')
    return elem

comp = []; space_group = []; oqmd_id = []; formation_energy = []; stability = []
n_atoms = []

def make_sym_coor(lis):
    sit = lis['sites']
    bas = [sit[i].split('@') for i in range(len(sit))]
    symbols = []; coordinate = []
    for i in range(len(bas)):
        sym = bas[i][0].split()[0]
        symbols.append(sym)
        coor = bas[i][1].split()
        coor_ = [float(coor[i]) for i in range(len(coor))]
        coordinate.append(coor_)
    return symbols, coordinate

def make_crys(lis):
    spg = lis['spacegroup']
    symbols, coordinate = make_sym_coor(lis)
    latt = lis['unit_cell']
    return Atoms(symbols=symbols, scaled_positions=coordinate, cell=latt)

curr_dir = os.getcwd()
#for i in range(5):
for i in range(len(all_list_elem)):
    print(extract_elem(all_list_elem[i]))
    with qr.QMPYRester() as q:
       kwargs = {
           'composition': extract_elem(all_list_elem[i]),
           'stability': '<0',            # hull distance smaller than -0.1 eV
           }
       list_of_data = q.get_oqmd_phases(**kwargs)
    
    print(len(list_of_data['data']))
    
    for  i in range(len(list_of_data['data'])):
         name = list_of_data['data'][i]['name']
         if os.path.exists(name):
            continue
         else:
            comp.append(name)
            space_group.append(list_of_data['data'][i]['spacegroup'])
            stability.append(list_of_data['data'][i]['stability'])
            formation_energy.append(list_of_data['data'][i]['delta_e'])
            oqmd_id.append(list_of_data['data'][i]['entry_id'])
            n_atoms.append(list_of_data['data'][i]['natoms'])
            struc = make_crys(list_of_data['data'][i])
            os.makedirs(name)
            path = curr_dir + '/' + name
            os.chdir(path)
            write('POSCAR', struc)
            struc_pm = Structure.from_file('POSCAR')
            v = MPRelaxSet(struc_pm, user_kpoints_settings={"reciprocal_density": 1000})
            v.write_input('./relax')
            os.chdir(curr_dir)

dict = {'composition': comp, 'space group':space_group, 'hull distance':stability, 
        'formation energy':formation_energy, 'oqmd id': oqmd_id, '# atoms': n_atoms}

df = pd.DataFrame(dict, columns=['composition','space group','# atoms','hull distance','formation energy','oqmd id'])
df.to_csv('list_stable-bulk_calcs.csv', index=False)
