#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 00:03:46 2018

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
from pymatgen import Structure, Lattice, MPRester, Molecule
from pymatgen.analysis.adsorption import *
from pymatgen.core.surface import generate_all_slabs
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from matplotlib import pyplot as plt
from ase.build import molecule

a = Structure.from_file('POSCAR')
b = AdsorbateSiteFinder(a)
ads_sites = b.find_adsorption_sites()
#fig = plt.figure()
#ax = fig.add_subplot(111)
#plot_slab(a, ax, adsorption_sites=True)

no = molecule("NO")
no_pos = no.get_positions()
#nh_pos = -nh_pos
#print nh3_pos

adsorbate = Molecule("NO", no_pos)
ads_structs = b.generate_adsorption_structures(adsorbate)
#print len(ads_structs)
for i in range(len(ads_structs)):
	f = 'POSCAR_' + str(i) + '.vasp' 
	ads_structs[i].to(filename=f)
#plot_slab(ads_structs[0], ax, adsorption_sites=False, decay=0.09)
