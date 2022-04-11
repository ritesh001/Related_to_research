
from pymatgen import Structure, Element
from pymatgen.io.vasp.sets import MPRelaxSet
from ase.io import read, write
import numpy as np

struc = Structure.from_file('POSCAR')
stru = read('POSCAR')
sym = stru.get_chemical_symbols()
#atom_num = struc.atomic_numbers
coords = struc.frac_coords
a = struc.lattice.a
b1 = 0.5*a
b2 = np.sqrt(3)*b1
c = struc.lattice.c
latt = [[a, 0.00, 0.00], [-b1, b2, 0.00], [0.00, 0.00, c]]
struc_new = Structure(latt, sym, coords)
struc_new.to('POSCAR')
v = MPRelaxSet(struc_new)
v.write_input('.')
