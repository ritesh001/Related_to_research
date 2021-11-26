# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 00:11:33 2020

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean

df1 = pd.read_csv('all-list.csv')
comp = df1['Compound']; comp_ = df1['Compound_']
ox_state = df1['M_oxid_state']
form_ener = df1['Formation_energy']

hard_file = pd.read_csv('hardness-values.csv', index_col='Ion')
# ion = hard_file['Ion']
# hardness = hard_file['Hardness']

cation_hard = []
min_anion_hard = []; max_anion_hard = []; mean_anion_hard = []; dev_anion_hard = []
min_diff_hard = []; max_diff_hard = []; mean_diff_hard = []; dev_diff_hard = []
all_hard_arr = []; amean_all_hard = []; gmean_all_hard = []

# for i in range(5):
for i in range(len(comp)):
    species = comp_[i].split('-')
    metal = species[2]
    metal_ox = metal + str(ox_state[i]) + '+'
    print(comp[i])
    ligand_1 = species[0]; ligand_2 = species[1]
    if ox_state[i] == 2:
        ligand_1_ox = ligand_1 + '1-'; ligand_2_ox = ligand_2 + '1-'
    elif ox_state[i] == 4:
        ligand_1_ox = ligand_1 + '2-'; ligand_2_ox = ligand_2 + '2-'
    elif ox_state[i] == 3:
        ligand_1_ox = ligand_1 + '2-'; ligand_2_ox = ligand_2 + '1-'
    ligands = [ligand_1_ox, ligand_2_ox]
    print(metal_ox, ligands)
    metal_hard = [hard_file.loc[metal_ox].item()]                               # Metal hardness; .item() necessary for pd.Series object
    cation_hard.append(metal_hard[0])
    ligands_hard = [hard_file.loc[ligand_1_ox].item(), hard_file.loc[ligand_2_ox].item()] # Ligand hardness
    # print(metal_hard, ligands_hard)
    min_anion_hard.append(min(ligands_hard)); max_anion_hard.append(max(ligands_hard))
    mean_anion_hard.append(np.mean(ligands_hard)); dev_anion_hard.append(np.std(ligands_hard))
    diff_hard = [(metal_hard[0] - ligands_hard[i]) for i in range(len(ligands))]
    min_diff_hard.append(min(diff_hard)); max_diff_hard.append(max(diff_hard))
    mean_diff_hard.append(np.mean(diff_hard)); dev_diff_hard.append(np.std(diff_hard))
    all_hard = metal_hard + ligands_hard
    all_hard_arr.append(all_hard)
    amean_all_hard.append(np.mean(all_hard))                                  # Arithmetic mean of hardness of all ions
    gmean_all_hard.append(gmean(all_hard))                              # Geometric mean of hardness of all ions
    
dict = {'Compound': comp, 'eta_cation': cation_hard, 'min_eta_anion': min_anion_hard,
        'max_eta_anion': max_anion_hard, 'mean_eta_anion': mean_anion_hard,
        'std-dev_eta_anion': dev_anion_hard, 'min_diff_eta': min_diff_hard,
        'max_diff_eta': max_diff_hard, 'mean_diff_eta': mean_diff_hard,
        'std-dev_diff_eta': dev_diff_hard, 'mean_eta_both': amean_all_hard,
        'geom-mean_eta_both': gmean_all_hard, 'eta_all': all_hard_arr,
        'Formation_energy': form_ener}
df = pd.DataFrame(dict, columns=['Compound', 'eta_cation', 'min_eta_anion', 'max_eta_anion',
                                  'mean_eta_anion', 'std-dev_eta_anion', 'min_diff_eta',
                                  'max_diff_eta', 'mean_diff_eta', 'std-dev_diff_eta',
                                  'mean_eta_both', 'geom-mean_eta_both', 'eta_all', 
                                 'Formation_energy'])
df.to_csv('hardness-features_all.csv', index=False)
df.to_json('hardness-features_all.json')
