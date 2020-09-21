# coding: utf-8
# Copyright (c) Henniggroup.
# Distributed under the terms of the MIT License.

from __future__ import division, print_function, unicode_literals, absolute_import
import sys

"""
Compute the reduced matching lattice vectors for heterostructure
interfaces as described in the paper by Zur and McGill:
Journal of Applied Physics 55, 378 (1984); doi: 10.1063/1.333084
"""

__author__ = "Kiran Mathew, Arunima Singh, Ritesh Kumar(modified for 2d-2d heterostructures)"

from mpinterfaces.calibrate import CalibrateSlab
from mpinterfaces.interface import Interface
from mpinterfaces.transformations import *
from mpinterfaces.utils import *

separation = 3  # in angstroms
nlayers_2d = 1
nlayers_substrate = 1


substrate_1 = slab_from_file([0, 0, 1], sys.argv[1])
sa_sub = SpacegroupAnalyzer(substrate_1)
substrate_2 = slab_from_file([0, 0, 1], sys.argv[2])

substrate_1_aligned, substrate_2_aligned = get_aligned_lattices(
    substrate_1,
    substrate_2,
    max_area=400,
    max_mismatch=0.05,
    max_angle_diff=1,
    r1r2_tol=0.01)
# substrate_1_aligned.to(fmt='poscar',
                          # filename='POSCAR_gr_aligned.vasp')
# substrate_2_aligned.to(fmt='poscar',
                      # filename='POSCAR_mos2_aligned.vasp')

# merge substrate and mat2d in all possible ways
hetero_interfaces = generate_all_configs(substrate_1_aligned,
                                         substrate_2_aligned,
                                         nlayers_2d, nlayers_substrate,
                                         separation)
# generate all poscars
for i, iface in enumerate(hetero_interfaces):
    poscar = Poscar(iface)
    poscar.write_file(
        filename='POSCAR_final_{}.vasp'.format(i))
