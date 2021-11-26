# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 00:17:42 2020

@author: ritesh
"""

from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty, Stoichiometry, ValenceOrbital, IonProperty
from matminer.featurizers.structure import (SiteStatsFingerprint, StructuralHeterogeneity,
                                            ChemicalOrdering, StructureComposition, MaximumPackingEfficiency)
from matminer.featurizers import composition as cf
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.conversions import DictToObject
import pandas as pd
from pymatgen import Structure
import os

feature_calculators = MultipleFeaturizer([cf.Stoichiometry(), cf.ElementProperty.from_preset("magpie"),
                                          cf.ValenceOrbital(props=['avg']), cf.IonProperty(fast=True)])
featurizer = MultipleFeaturizer([
    SiteStatsFingerprint.from_preset("CoordinationNumber_ward-prb-2017"),
    StructuralHeterogeneity(),
    ChemicalOrdering(),
    SiteStatsFingerprint.from_preset("LocalPropertyDifference_ward-prb-2017"),
    StructureComposition(Stoichiometry()),
    StructureComposition(ElementProperty.from_preset("magpie")),
    StructureComposition(ValenceOrbital(props=['avg'])),
    StructureComposition(IonProperty(fast=True))
])
#feature_labels = feature_calculators.feature_labels()
#print(len(feature_labels))

data_or = pd.read_csv('form-ener_scan_II_X-Y-1_d.csv')
comp = data_or['Compound']
images = []
curr_dir = os.getcwd()
for i in range(3):
#for i in range(len(comp)):
	print(comp[i])
	path = curr_dir + '/' + comp[i]
	os.chdir(path)
	struc = Structure.from_file('POSCAR')
	images.append(struc)
	os.chdir(curr_dir)
	
#data = StrToComposition(target_col_id='composition_obj').featurize_dataframe(data_or, 'Compound')
#data = feature_calculators.featurize_dataframe(data, col_id='composition_obj')

#dto = DictToObject(target_col_id='structure', overwrite_data=True)
#data = dto.featurize_dataframe(data_orig, 'structure')
#print('Total number of features:', len(featurizer.featurize(data['structure'][0])))
#print('Total number of features:', len(feature_calculators.featurize(data['composition_obj'][0])))
	
data = featurizer.featurize_many(images, ignore_errors=True)
print(len(data))
data.to_csv('feat_II_X-Y-1_d.csv')
