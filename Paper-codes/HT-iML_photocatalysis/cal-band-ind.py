from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from pymatgen.io.vasp import Vasprun
import os, sys

curr_dir = os.getcwd()
comp = []
with open('lvhar','r') as f:
     a = f.readlines()
     comp = [a[i].split()[0] for i in range(len(a))]

vbm_ki = [0 for i in range(len(comp))]; cbm_ki = [0 for i in range(len(comp))]
vbm_k = [0 for i in range(len(comp))]; cbm_k = [0 for i in range(len(comp))]
vbm_b = [0 for i in range(len(comp))]; cbm_b = [0 for i in range(len(comp))]
for i in range(len(comp)):
    path = curr_dir + '/' + str(comp[i])
    os.chdir(path)
    print(comp[i])
    dosrun = Vasprun("vasprun.xml")
    a = dosrun.get_band_structure() 
    b = a.get_band_gap() 
    vb = a.get_vbm()
    cb = a.get_cbm()
    vb_ki = vb['kpoint_index'][0] + 1   ## numbering in python starts from 0
    cb_ki = cb['kpoint_index'][0] + 1
    vb_k = vb['kpoint'].frac_coords
    cb_k = cb['kpoint'].frac_coords
    vbm_ki[i] = vb_ki; cbm_ki[i] = cb_ki
    vbm_k[i] = vb_k; cbm_k[i] = cb_k
    
    for it in cb['band_index'].items():
        cb_b = it[1][0] + 1
    vb_b = cb_b - 1
    vbm_b[i] = vb_b; cbm_b[i] = cb_b
    #print("k-point index of vbm = ", vb_k)
    #print("k-point index of cbm = ", cb_k)
    #print("band index of vbm = ", vb_b)
    #print("band index of cbm = ", cb_b)
    
    f = open("KPOINTS","w")
    f.write("Automatically generated mesh\n")
    kpoint = a.kpoints
    f.write("{}\n".format(len(kpoint)))
    f.write("Reciprocal lattice\n")
    for i in range(len(kpoint)):
        #f.write("{.4f} {.4f} {.4f}\n".format(kpoint[i].frac_coords[0],kpoint[i].frac_coords[1],kpoint[i].frac_coords[2]))
        f.write("{} {} {} 0.003\n".format(kpoint[i].frac_coords[0],kpoint[i].frac_coords[1],kpoint[i].frac_coords[2]))
    f.close()
    
    f0 = open("INCAR", "w")
    f0.write("EDIFF = 1e-08\n")
    f0.write("ICHARG = 11\n")
    f0.write("ISTART = 2\n")
    f0.write("ENCUT = 500\n")
    f0.write("IBRION = 2\n")
    f0.write("ISMEAR = 0\n")
    f0.write("ISPIN = 2\n")
    f0.write("NSW = 0\n")
    f0.write("SIGMA = 0.01\n")
    f0.write("IDIPOL = 3\n")
    f0.write("LPARD = .TRUE.\n")
    f0.write("LSEPB = .TRUE.\n")
    f0.write("LSEPK = .TRUE.\n")
    f0.write("IBAND = {} {}\n".format(vb_b, cb_b))
    f0.write("KPUSE = {} {}\n".format(vb_ki, cb_ki))
    f0.close()
    os.chdir(curr_dir)

dict = {'Compound': comp, 'VBM_kpoint_ind': vbm_ki, 'CBM_kpoint_ind': cbm_ki, 'VBM_kpoint': vbm_k, 'CBM_kpoint':cbm_k, 'VBM_band_ind':vbm_b, 'CBM_band_ind':cbm_b}
df = pd.DataFrame(dict, columns=['Compound', 'VBM_kpoint_ind', 'CBM_kpoint_ind', 'VBM_kpoint','CBM_kpoint','VBM_band_ind','CBM_band_ind'])
df.to_csv('vbm-cbm_indices_pbe.csv', index=False)
df.to_json('vbm-cbm_indices_pbe.json')
