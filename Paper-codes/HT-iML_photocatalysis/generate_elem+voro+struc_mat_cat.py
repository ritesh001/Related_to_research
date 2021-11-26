# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 00:17:42 2020

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty, Stoichiometry, ValenceOrbital, IonProperty, OxidationStates, ElectronegativityDiff, ElectronAffinity
from matminer.featurizers.structure import (SiteStatsFingerprint, StructuralHeterogeneity,
                                            ChemicalOrdering, StructureComposition, DensityFeatures, RadialDistributionFunction, PartialRadialDistributionFunction, ElectronicRadialDistributionFunction, JarvisCFID)
#from matminer.featurizers import composition as cf
from matminer.featurizers.conversions import StrToComposition, StructureToOxidStructure
from matminer.featurizers.conversions import DictToObject
from catlearn.fingerprint.voro import VoronoiFingerprintGenerator
import pandas as pd
from pymatgen import Structure
from ase.io import read
import numpy as np
import os

## Elemental + Structural features -- requires structures ##
featurizer = MultipleFeaturizer([
## Structural features
    DensityFeatures(),
    SiteStatsFingerprint.from_preset("CrystalNNFingerprint_cn"),
## Elemental features
    StructureComposition(Stoichiometry()),
#    StructureComposition(ElementProperty.from_preset("magpie")),
#    StructureComposition(ValenceOrbital(props=['avg'])),
#    StructureComposition(IonProperty(fast=True)),
#    StructureComposition(OxidationStates()),
    StructureToOxidStructure(OxidationStates()),
    StructureComposition(ElectronegativityDiff()),
    StructureComposition(ElectronAffinity())
])

data_or = pd.read_csv('form-ener_scan_all.csv')
comp = data_or['Compound']
images = []; images_ase = []
curr_dir = os.getcwd()
#for i in range(10):
for i in range(len(comp)):
    print(comp[i])
    path = curr_dir + '/' + comp[i]
    os.chdir(path)
    struc = Structure.from_file('POSCAR')
    struc_ase = read('POSCAR')
    images.append(struc)
    images_ase.append(struc_ase)
    os.chdir(curr_dir)

dict = {'Compound':comp, 'structure':images}
df = pd.DataFrame(dict)
dto = DictToObject(target_col_id='structure', overwrite_data=True)
data = dto.featurize_dataframe(df, 'structure')

comp_id = []
comp_arr = np.array(comp)
df_all = pd.read_json('all-list_comp.json')
for i in range(len(df_all['Compound'])):
    if df_all['Compound'][i] in comp_arr:
       #print(df_all['Compound_id'][i])
       comp_id.append(df_all['Compound_id'][i])
	
feat = featurizer.featurize_dataframe(data, 'structure', ignore_errors=True)
feat.drop(['structure'], axis=1, inplace=True)
feat['Compound_id'] = comp_id
feat['Formation_energy'] = data_or['H_f']

fing = VoronoiFingerprintGenerator(images_ase)
fing.write_voro_input()
fing.run_voro()
voro = fing.generate()
for col in voro.columns:
    feat[col] = voro[col]

feat.to_csv('elem+voro+struc_feat_all.csv', index=False)
feat_label = feat.columns
l = len(feat_label)
print(l)
