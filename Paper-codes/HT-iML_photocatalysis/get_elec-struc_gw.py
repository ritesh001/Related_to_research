from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from pymatgen.io.vasp import Vasprun
import os, sys

curr_dir = os.getcwd()
comp = []
with open('list_all','r') as f:
     a = f.readlines()
     comp = [a[i].split()[0] for i in range(len(a))]

#comp = comp_a[5:10]

bandgap = [0 for i in range(len(comp))]
vbm = [0 for i in range(len(comp))] 
cbm = [0 for i in range(len(comp))]
for i in range(len(comp)):
    path = curr_dir + '/' + str(comp[i])
    os.chdir(path)
    print(comp[i])
    dosrun = Vasprun("vasprun.xml")
    a = dosrun.get_band_structure() 
    b = a.get_band_gap() 
    c = a.is_metal()
    vb = a.get_vbm()['energy']
    cb = a.get_cbm()['energy']
    if c == True:
       bandgap[i] = 0.0
       vbm[i] = 'NA'
       cbm[i] = 'NA'
    elif c == False:
       bandgap[i] = b['energy']
       vbm[i] = vb
       cbm[i] = cb
    #print(b)
    os.chdir(curr_dir)

dict = {'Compound': comp, 'Bandgap': bandgap, 'VBM (absolute)': vbm, 'CBM (absolute)': cbm}
df = pd.DataFrame(dict, columns=['Compound', 'Bandgap', 'VBM (absolute)', 'CBM (absolute)'])
df.to_csv('elec-struc_gw_pbe_htd.csv', index=False)
