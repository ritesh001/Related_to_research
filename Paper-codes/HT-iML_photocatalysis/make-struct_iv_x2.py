#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore")
from pymatgen import Element
from pymatgen.io.vasp.sets import latt_opt
from pymatgen.io.vasp import Structure

struc = Structure.from_file('POSCAR')
dop = ['Ti', 'Ge', 'Sn', 'Hf', 'Mo', 'Tc', 'W', 'Os', 'Pd', 'Pt', 'Ru', 'Te', 'Ce', 'Re', 'Ir']


for dopants in dop:
	struc.replace_species({Element("Zr"): Element(dopants)})
	v = latt_opt(struc)
	dir_name = str(dopants) + '/' + 'latt-opt'
	v.write_input(dir_name)
	struc = Structure.from_file('POSCAR')
