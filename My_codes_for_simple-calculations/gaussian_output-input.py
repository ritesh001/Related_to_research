#!/usr/bin/env python
"""Use it for restarting a Gaussian calculation ..."""
"""... from earlier run"""
"""Run it as python gaussian_output-input.py <name of log file>"""

import pymatgen
from pymatgen.io.gaussian import Molecule, GaussianOutput, GaussianInput
import warnings
warnings.filterwarnings("ignore")
import sys
import os

output_file = sys.argv[1]
curr_dir = os.getcwd()
a = GaussianOutput(sys.argv[1])
b = a.final_structure

c = output_file.split('.')
input_file = c[0] + '.com'
gau = GaussianInput(b,
title='kickstruct', functional='b3lyp', basis_set='lanl2dz',             # change it accordingly
link0_parameters={"%nprocshared": "4", "%mem": "30GB"},                  # change it accordingly
route_parameters={"opt": "", "scf": "qc"})
gau.write_file(input_file)
