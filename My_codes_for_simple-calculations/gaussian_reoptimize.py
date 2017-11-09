#!/usr/bin/env python
"""Use this code for converting output files of Gaussian with error ..."""
"""... termination into input file for reoptimization"""

from pymatgen.io.gaussian import Molecule, GaussianInput, GaussianOutput
import warnings
warnings.filterwarnings("ignore")
import sys
import os
from shutil import copyfile

output_file = sys.argv[1]
curr_dir = os.getcwd(); next_dir = curr_dir + '/reoptimize'
a = GaussianOutput(sys.argv[1])
b = a.errors

## Checking for error files and copying to 'reoptimize' folder
if 'Optimization error' in b:
    copyfile(curr_dir + '/' + output_file, next_dir + '/' + output_file)
    c = a.final_structure
    d = output_file.split('.')
    input_file = d[0] + '.com'
    gau = GaussianInput(c,
    title='kickstruct', functional='', basis_set='',                            # change it accordingly
    link0_parameters={"%nprocshared": "4", "%mem": "1GB"},
    route_parameters={"opt": "", "pm6": "", "scf": "qc"})                       # change it accordingly
    os.chdir(next_dir)
    gau.write_file(input_file)

os.chdir(curr_dir)
