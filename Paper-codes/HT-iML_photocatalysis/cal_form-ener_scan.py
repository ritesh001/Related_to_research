import os
import numpy as np
import pandas as pd
from matminer.featurizers.structure import OrbitalFieldMatrix
from pymatgen import Structure
from ase.io import read

images = []
curr_dir = os.getcwd()
with open('list_III_X-Y_2_done','r') as f:
     a = f.readlines()
f.close()

def read_poscar(file):
	f0 = open('POSCAR','r')
	b = []
	for line in f0:
		a = line.split()
		a = [a[i] for i in range(len(a))]
		b.append(a)
	f0.close()
	atoms = []
	atoms_number = []
	for j in range(len(b[5])):
		atoms.append(b[5][j])
		atoms_number.append(int(b[6][j]))
	return atoms, atoms_number

ref = pd.read_csv('all-ref_scan.csv')
def sum_ref_energies(sym, number):
	s = 0
	for i in range(len(sym)):
		s += number[i] * float(ref[ref['Element'] == sym[i]]['Energy/atom'])
	return s
		
comp = []
for i in range(len(a)):
    path = curr_dir + '/' + a[i].split()[0] + '/'
    comp.append(a[i].split('/')[0])
    os.chdir(path)
    print(path)
    sym, number = read_poscar('POSCAR')
    print(sym, number)
    out = read('OUTCAR')
    tot_energy = out.get_total_energy()
    print(tot_energy)
    os.chdir(curr_dir)
    ref_tot = sum_ref_energies(sym, number)
    formation_energy = tot_energy - ref_tot
    formation_energy /= sum(number)
    print(formation_energy)
	

#dict = {'Compound': comp}
#df = pd.DataFrame(dict)
#feat = [[[] for i in range(ofm_l)] for j in range(len(images))]
#for i in range(len(images)):
#	for j in range(ofm_l):
#		feat[i][j] = ofm.featurize(images[i])[j]
#
#feat = np.array(feat)		
#for i in range(ofm_l):
#	feat_ind = 'feature-' + str(i+1)
#	df[feat_ind] = feat.T[i]
#df['formation_energy'] = form_ener
#df.to_csv('data_ofm.csv', index=False)
