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

curr_dir = os.getcwd()

a = Structure.from_file('POSCAR')
b = AdsorbateSiteFinder(a)
ads_sites = b.find_adsorption_sites()
#fig = plt.figure()
#ax = fig.add_subplot(111)
#plot_slab(a, ax, adsorption_sites=True)

co2 = molecule("CO2")
co2.rotate(90,'y')
co2_pos = co2.get_positions()
# oh_pos = -oh_pos
#print nh3_pos

adsorbate = Molecule("COO", co2_pos)
ads_structs = b.generate_adsorption_structures(adsorbate)
#print len(ads_structs)
for i in range(len(ads_structs)):
	path = curr_dir + '/' + str(i)
	os.makedirs(path)
	os.chdir(path)
	f = 'POSCAR'
	# f = 'POSCAR_' + str(i) + '.vasp' 
	ads_structs[i].to(filename=f)
	copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
	copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
	copyfile(curr_dir + '/' + 'POTCAR' , path + '/' + 'POTCAR')
	os.chdir(curr_dir)

#plot_slab(ads_structs[0], ax, adsorption_sites=False, decay=0.09)
