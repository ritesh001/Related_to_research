
import warnings
warnings.filterwarnings('ignore')
from pymatgen import Structure, Element
from pymatgen.io.vasp.sets import MPRelaxSet
from ase.io import read, write
import numpy as np
import os
from shutil import copyfile

with open('redo','r') as f:
#with open('send-tue_60','r') as f:
     w = f.readlines()
f.close()

curr_dir = os.getcwd()

for i in range(len(w)):
    #path = curr_dir + '/' + a[i].split('/')[0]
    path = curr_dir + '/' + w[i].split()[0]
    os.chdir(path)
    print(w[i].split()[0])
    struc = Structure.from_file('POSCAR')
    stru = read('POSCAR')
    sym = stru.get_chemical_symbols()
    #atom_num = struc.atomic_numbers
    coords = struc.frac_coords
    a = struc.lattice.a
    b1 = np.float32(0.5*a)
    b2 = np.sqrt(3)*b1
    c = struc.lattice.c
    latt = [[a, 0.00, 0.00], [-b1, b2, 0.00], [0.00, 0.00, c]]
    struc_new = Structure(latt, sym, coords)
    struc_new.to('POSCAR')
    v = MPRelaxSet(struc_new,user_potcar_settings = {'Ac': 'Ac', 'Ag': 'Ag', 'Al': 'Al', 'Ar': 'Ar',
	'As': 'As', 'Au': 'Au', 'B': 'B', 'Ba': 'Ba_sv', 'Be': 'Be_sv', 
	'Bi': 'Bi', 'Br': 'Br', 'C': 'C', 'Ca': 'Ca_sv', 'Cd': 'Cd', 
	'Ce': 'Ce_3', 'Cl': 'Cl', 'Co': 'Co', 'Cr': 'Cr_pv', 'Cs': 'Cs_sv', 
	'Cu': 'Cu_pv', 'Dy': 'Dy_3', 'Er': 'Er_3', 'Eu': 'Eu_3', 'F': 'F', 
	'Fe': 'Fe_pv', 'Ga': 'Ga_d', 'Gd': 'Gd_3', 'Ge': 'Ge_d', 'H': 'H', 
	'He': 'He', 'Hf': 'Hf_pv', 'Hg': 'Hg', 'Ho': 'Ho_3', 'I': 'I', 
	'In': 'In_d', 'Ir': 'Ir', 'K': 'K_sv', 'Kr': 'Kr', 'La': 'La', 
	'Li': 'Li_sv', 'Lu': 'Lu_3', 'Mg': 'Mg_pv', 'Mn': 'Mn_pv', 
	'Mo': 'Mo_pv', 'N': 'N', 'Na': 'Na_pv', 'Nb': 'Nb_pv', 'Nd': 'Nd_3', 
	'Ne': 'Ne', 'Ni': 'Ni_pv', 'Np': 'Np', 'O': 'O', 'Os': 'Os_pv', 
	'P': 'P', 'Pa': 'Pa', 'Pb': 'Pb_d', 'Pd': 'Pd', 'Pm': 'Pm_3', 
	'Pr': 'Pr_3', 'Pt': 'Pt', 'Pu': 'Pu', 'Rb': 'Rb_sv', 'Re': 'Re_pv', 
	'Rh': 'Rh_pv', 'Ru': 'Ru_pv', 'S': 'S', 'Sb': 'Sb', 'Sc': 'Sc_sv', 
	'Se': 'Se', 'Si': 'Si', 'Sm': 'Sm_3', 'Sn': 'Sn_d', 'Sr': 'Sr_sv', 
	'Ta': 'Ta_pv', 'Tb': 'Tb_3', 'Tc': 'Tc_pv', 'Te': 'Te', 'Th': 'Th', 
	'Ti': 'Ti_pv', 'Tl': 'Tl_d', 'Tm': 'Tm_3', 'U': 'U', 'V': 'V_pv', 
	'W': 'W_pv', 'Xe': 'Xe', 'Y': 'Y_sv', 'Yb': 'Yb_2', 'Zn': 'Zn', 'Zr': 'Zr_sv'})
    v.write_input('.')
    copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
    copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
    os.chdir(curr_dir)
