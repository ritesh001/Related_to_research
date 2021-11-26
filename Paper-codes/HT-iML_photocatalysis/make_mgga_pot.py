from pymatgen.io.vasp.sets import latt_opt
from pymatgen import Structure

stru = Structure.from_file('POSCAR')
v = latt_opt(stru)
v.write_input('./')
