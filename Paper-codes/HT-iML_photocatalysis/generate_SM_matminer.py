import os
import numpy as np
import pandas as pd
from matminer.featurizers.structure import SineCoulombMatrix
from pymatgen import Structure

images = []
curr_dir = os.getcwd()
#with open('list_all','r') as f:
#with open('list_III_X-Y_2_done','r') as f:
#     a = f.readlines()
#f.close()

## Uncomment above lines when reading from list files
file = pd.read_csv('fin_voro_data.csv')
comp = file['Compound']
form_ener = file['formation_energy']

#comp = []                                                                     # uncomment when not reading from df
for i in range(len(comp)):
	path = curr_dir + '/' + comp[i]
#    path = curr_dir + '/' + a[i].split()[0]                                   # uncomment when not reading from df
#    comp.append(a[i].split('/')[0])                                           # uncomment when not reading from df
	os.chdir(path)
	atoms = Structure.from_file('POSCAR')
	images.append(atoms)
	os.chdir(curr_dir)
	
sm = SineCoulombMatrix(flatten=True)
sm.fit(images)
sm_l = len(sm.featurize(images[0]))

dict = {'Compound': comp}
df = pd.DataFrame(dict)
feat = [[[] for i in range(sm_l)] for j in range(len(images))]
for i in range(len(images)):
	for j in range(sm_l):
		feat[i][j] = sm.featurize(images[i])[j]

feat = np.array(feat)		
for i in range(sm_l):
	feat_ind = 'feature-' + str(i+1)
	df[feat_ind] = feat.T[i]
df['formation_energy'] = form_ener
df.to_csv('data_sm.csv', index=False)
