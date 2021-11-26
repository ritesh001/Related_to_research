#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore")
from pymatgen import Element
from pymatgen.io.vasp.sets import latt_opt
from pymatgen.io.vasp import Structure

struc = Structure.from_file('POSCAR')
dop = ['Al', 'Ga', 'In', 'Ru', 'Y', 'La', 'Bi','Rh', 'Cr', 'Sc']
dop += ['Ce', 'Co', 'Fe', 'Gd', 'Ir', 'Lu', 'Nd', 'Sm']


for dopants in dop:
	struc.replace_species({Element("Fe"): Element(dopants)})
	v = latt_opt(struc)
	dir_name = str(dopants) + '/' + 'latt-opt'
	v.write_input(dir_name)
	struc = Structure.from_file('POSCAR')
