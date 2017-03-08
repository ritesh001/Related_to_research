from ase import Atoms
from ase.build import fcc100, add_adsorbate
from ase.structure import molecule
from ase.io import write
from ase.visualize import view

slab = fcc100('Pt', size=(4,4,2), vacuum=10.0)

atoms = molecule('CO')
#atoms.translate([5.10531096,0,0])
atoms.center()

h = 3.0

add_adsorbate(slab, atoms, h, 'ontop')

#print slab.get_positions()
#write('CO-on-Pt_100.vasp', slab)
view(slab, viewer='VMD')
