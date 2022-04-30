#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 00:03:46 2018

@author: ritesh
"""

import warnings, sys, os
warnings.filterwarnings('ignore')
from pymatgen import Structure, Lattice, MPRester, Molecule
from pymatgen.analysis.adsorption import *
from pymatgen.core.surface import generate_all_slabs
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from matplotlib import pyplot as plt
from ase.build import molecule
from shutil import copyfile
import pandas as pd
from ase.io import read

curr_dir = os.getcwd()

a = Structure.from_file('POSCAR')
b = AdsorbateSiteFinder(a)
ads_sites = b.find_adsorption_sites()
#fig = plt.figure()
#ax = fig.add_subplot(111)
#plot_slab(a, ax, adsorption_sites=True)

cooh = read('cooh-rot.vasp')
#cooh.rotate(90,'x')
#cooh.rotate(90)
pos = cooh.get_positions()

for i in range(4):
      pos[i][0] -= 13.5409450000000007
      pos[i][1] -= 14.2590830000000004
      pos[i][2] -= 12.5000000000000000

pos = -pos
#print nh3_pos

adsorbate = Molecule("OOCH", pos)
ads_structs = b.generate_adsorption_structures(adsorbate)
#print len(ads_structs)
index = []; index_tot = []; ads_type_all = []
ontop_b = np.isin(ads_sites['all'], ads_sites['ontop'])
bridge_b = np.isin(ads_sites['all'], ads_sites['bridge'])
hollow_b = np.isin(ads_sites['all'], ads_sites['hollow'])
ontop_ind = [i for i in range(len(ontop_b)) if ontop_b[i][0] == True]
bridge_ind = [i for i in range(len(bridge_b)) if bridge_b[i][0] == True]
hollow_ind = [i for i in range(len(hollow_b)) if hollow_b[i][0] == True]
ads_type = []
for i in range(len(ads_structs)):
	path = curr_dir + '/' + str(i)
	os.makedirs(path)
	os.chdir(path)
	f = 'POSCAR'
	# f = 'POSCAR_' + str(i) + '.vasp' 
	ads_structs[i].to(filename=f)
	copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
	if i in ontop_ind:
		ads_type.append('ontop'); ads_type_all.append('ontop')
	elif i in bridge_ind:
		ads_type.append('bridge'); ads_type_all.append('bridge')
	elif i in hollow_ind:
		ads_type.append('hollow'); ads_type_all.append('hollow')
	os.chdir(curr_dir)

#plot_slab(ads_structs[0], ax, adsorption_sites=False, decay=0.09)
df1 = pd.DataFrame()
df1['adsorbate type'] = ads_type
df1.to_csv('check_ads-type.csv')
