#!/usr/bin/env python
__author__ = 'Ritesh Kumar'

"""Use this code for generating surface for the catalytic applications"""

from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Structure, Lattice
from pymatgen.io.vasp import Poscar, Outcar
from pymatgen.io.vasp.sets import single_point_crude
# from pymatgen.io.vasp.sets import dos_pbe
from ase.io import read, write
from ase.build import surface

"""Making supercell using ASE module (some problem with pymatgen module)"""
bulk = read('POSCAR')
slab = surface(bulk, (1,0,0), 3)
slab.center(vacuum=6, axis=2)
write('POSCAR', slab)

"""Making supercell and writing input files using pymatgen module"""
transformation_matrix = [[2,0,0],[0,2,0],[0,0,1]]
struct = Structure.from_file('POSCAR')
struct.make_supercell(transformation_matrix, to_unit_cell=True)
v = single_point_crude(struct)
# v = dos_pbe(struct)
v.write_input('single_point')
