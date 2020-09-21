#!/usr/bin/env python

"""Use it for generating symmetrized cif from normal cif"""
"""First convert POSCAR file to cif file from VESTA"""
"""Use it as python symmetrized_cif.py <cif file>"""

import pymatgen as pm
from pymatgen.io.cif import CifWriter
import sys

struct = pm.Structure.from_file(sys.argv[1])
w = CifWriter(struct, symprec=0.1)
w.write_file('symmetrized.cif')
