from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from pymatgen.io.vasp import Vasprun
import os, sys

curr_dir = os.getcwd()
#df1 = pd.read_json('form-ener_scan_all_corr.json')
df1 = pd.read_csv('form-ener_scan_all_corr.csv')
comp = df1['Compound']
#comp = comp_a[5:10]

comp_class = [0 for i in range(len(comp))]
bandgap = [0 for i in range(len(comp))]
gap_nature = [0 for i in range(len(comp))] 
transition = [0 for i in range(len(comp))]
for i in range(len(comp)):
    path = curr_dir + '/' + str(comp.iloc[i])
    os.chdir(path)
    print(comp.iloc[i])
    dosrun = Vasprun("vasprun.xml")
    a = dosrun.get_band_structure() 
    b = a.get_band_gap() 
    c = a.is_metal()
    if c == True:
       comp_class[i] = 'Metal'
       bandgap[i] = 0.0
       gap_nature[i] = 'NA'
       transition[i] = 'NA'
    elif c == False:
       comp_class[i] = 'Non-metal'
       bandgap[i] = b['energy']
       if b['direct'] == 'True':
          gap_nature[i] = 'Direct'
       else:
          gap_nature[i] = 'Indirect'
       transition[i] = b['transition']
    #print(b)
    os.chdir(curr_dir)

dict = {'Compound': comp, 'Class': comp_class, 'Bandgap': bandgap, 'Bandgap_nature': gap_nature, 'Kpoints_edge': transition}
df = pd.DataFrame(dict, columns=['Compound', 'Class', 'Bandgap', 'Bandgap_nature', 'Kpoints_edge'])
df.to_json('elec-struc_dos_pbe_all.json')
df.to_csv('elec-struc_dos_pbe_all.csv', index=False)
