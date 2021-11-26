# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 07:02:14 2020

@author: ritesh
"""

from pymatgen import Structure
from pymatgen.io.vasp.sets import MPRelaxSet
import sys

transformation_matrix = [[2,0,0],[0,2,0],[0,0,1]]
struct = Structure.from_file('POSCAR')
struct.make_supercell(transformation_matrix, to_unit_cell=True)
v = MPRelaxSet(struct)
#dir_name = sys.argv[1]
v.write_input('.')
