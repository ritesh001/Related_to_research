#!/usr/bin/env python
"""Use it for converting POSCAR file to gaussian input file"""
"""First convert POSCAR/CONTCAR to xyz file from VESTA"""

import pymatgen
from pymatgen.io.gaussian import Molecule, GaussianInput
from pymatgen.io.vasp import Structure, Poscar
from pymatgen.io.xyz import XYZ

## Change the following section accordingly and carefully! ##
new_struc = XYZ.from_file("3-pbe_scf.xyz")                                      # name of xyz file
tit = '3_water_gas_phase'                                                       # title of input file
func = 'pbepbe'                                                                 # name of functional used
bas = 'aug-cc-pvqz'                                                             # name of basis set used, not needed for semi-empirical calculations
gau = GaussianInput(new_struc.molecule,
#charge=1, spin_multiplicity=2,                                                 # uncomment it, if default values are not be used
title=tit, functional=func, basis_set=bas,                                      # remove only basis_set, if not necessary
link0_parameters={"%nprocshared": "4", "%mem": "50GB"},                         # nprocshared = required number of processors
route_parameters={"opt": "", "scf": "qc", "nosymm": ""})                        # edit this line very carefully
gau.write_file('3-pbe_scf.com')                                                 # name of input file to be generated
