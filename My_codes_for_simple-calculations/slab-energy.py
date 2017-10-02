#!/usr/bin/env python
"""Use it for calculating surface energies for slabs generated from bulk"""

from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Structure, Lattice
from pymatgen.io.vasp import Poscar, Outcar
import os
import re
import math as m

path = os.getcwd()
struct = Structure.from_file('POSCAR')
all_slabs = generate_all_slabs(struct, 3, 7, 8)

## Function for calculating number of species ##
def species_num(poscar):
    pos = Structure.from_file(poscar)
    form = pos.formula
    num = re.findall(r'\d+', form)
    num = [float(num[i]) for i in range(len(num))]
    s = 0
    for i in range(len(num)):
        s += num[i]
    return s

## Function for calculating surface area of a slab ##
def sur_area(poscar):
    pos = Structure.from_file(poscar)
    a = pos.lattice.a
    b = pos.lattice.b
    angle = pos.lattice.gamma
    angle *= (m.pi/180)
    area = 0.5 * b * a * m.sin(angle)
    return area

## -------------------------------------------------------------------- ##
path3 = path + '/single_point'
os.chdir(path3)
out = Outcar('OUTCAR')
bulk_energy = out.final_energy
a = species_num('POSCAR')
conversion_factor = 1.60218e1

for i in range(len(all_slabs)):
    h = all_slabs[i].miller_index[0]
    k = all_slabs[i].miller_index[1]
    l = all_slabs[i].miller_index[2]
    dirname = 'slab_' + str(h) + str(k) + str(l)
    path2 = path + '/' + dirname
    os.chdir(path2)
    out = Outcar('OUTCAR')
    b = species_num('POSCAR')
    c = b / a
    slab_energy = out.final_energy
    surface_energy = slab_energy - (c * bulk_energy)
    surface_area = sur_area('POSCAR')
    surface_energy /= (2 * surface_area)
    surface_energy *= conversion_factor
    print "%10s %12.8f" %(dirname, surface_energy)
## --------------------------------------------------------------------- ##
