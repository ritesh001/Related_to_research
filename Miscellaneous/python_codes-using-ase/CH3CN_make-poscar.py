import ase
#from ase import Atoms
from ase.structure import molecule
from ase.io import write

atoms = molecule('CH3CN')

atoms.center(vacuum = 7)

#print atoms.get_positions()                               #to get coordinates of atoms in cartesian coordinates
#print atoms.get_scaled_positions()                        #to get coordinates of atoms in reduced coordinates
write('CH3CN.vasp', atoms)                                 #to print structure in vasp format
