#!/usr/bin/env python
"""Use it for converting gaussian input files to POSCAR"""
"""Run it as:"""
"""python gaussian-poscar.py <name of gaussian file> <length of cubic box>"""

import pymatgen as pm
from pymatgen.io.gaussian import Molecule
from pymatgen.io.vasp import Structure
import sys

struc = Molecule.from_file(sys.argv[1])
lat = float(sys.argv[2])
new_struct = struc.get_boxed_structure(a=lat, b=lat, c=lat)
new_struct.to(filename="POSCAR")
