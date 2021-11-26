
import warnings
warnings.filterwarnings('ignore')
from pymatgen import Structure, Element
from pymatgen.io.vasp.sets import MPRelaxSet
from ase.io import read, write
import numpy as np
import os
from shutil import copyfile

with open('todo-plank','r') as f:
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
    v = MPRelaxSet(struc_new)
    v.write_input('.')
    copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
    copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
    os.chdir(curr_dir)
