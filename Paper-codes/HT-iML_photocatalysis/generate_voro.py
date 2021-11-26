from ase.io import read, write
import os
import numpy as np
import pandas as pd
from catlearn.featurize.setup import FeatureGenerator

images = []
curr_dir = os.getcwd()
with open('list_all','r') as f:
     a = f.readlines()
f.close()

comp = []
for i in range(len(a)):
    path = curr_dir + '/' + a[i].split()[0]
    comp.append(a[i].split()[0])
    os.chdir(path)
    atoms = read('POSCAR')
    images.append(atoms)
    os.chdir(curr_dir)

from catlearn.featurize.adsorbate_prep import autogen_info
#images = autogen_info(images)

from catlearn.fingerprint.voro import VoronoiFingerprintGenerator
fing = VoronoiFingerprintGenerator(images)
fing.write_voro_input()
fing.run_voro()
df = fing.generate()
df['Compound'] = comp
df.to_csv('data_voro.csv')
