import ase
from ase.structure import molecule
from ase.io import write

atoms1 = molecule('HCl')
atoms2 = molecule('NH3')

atoms2.translate([2.5,2.5,0])

bothatoms = atoms1 + atoms2
bothatoms.center(5)

write('NH3-HCl.vasp', bothatoms)
