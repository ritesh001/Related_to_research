#!/usr/bin/env python
"""Use it for generating all possible slabs for a given bulk structure"""

## Import the neccesary tools to generate surfaces
from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Structure, Lattice
# Import the neccesary tools for making a Wulff shape
from pymatgen.analysis.wulff import WulffShape
import os

struct = Structure.from_file('POSCAR')

""" Not required, just for testing """
## -------------------------------------------------------------------- ##
## We'll use the SlabGenerator class to get a single slab. We'll start with the
## (111) slab of material. Plug in the CONVENTIONAL unit cell of your structure, the
## maximum Miller index value to generate the different slab orientations along
## with the minimum slab and vacuum size in Angstroms
# slabgen = SlabGenerator(struct, (1,1,1), 4, 10)

## If we want to find all terminations for a particular Miller index orientation,
## we use the get_slabs() method. This returns a LIST of slabs rather than a single
## slab. When generating a slab for a particular orientation, there are sometimes
## more than one location we can terminate or cut the structure to create a slab. The
## simplest example of this would be the Si(Fd-3m) (111) slab which can be cut or
## terminated in two different locations along the vector of the Miller index. For a
## fcc structure such as Ni however, there should only be one way to cut a (111) slab.
# all_slabs = slabgen.get_slabs()
# print "The material(111) slab only has %s termination" %(len(all_slabs))
## -------------------------------------------------------------------- ##

## The simplest way to do this is to just use generate_all_slabs which finds all the unique
## Miller indices for a structure and uses SlabGenerator to create all terminations for all of them.
all_slabs = generate_all_slabs(struct, 3, 7, 8)
# print("%s unique slab structures have been found for a max Miller index of 3" %(len(all_slabs)))

"""To generate POSCAR files of slabs generated"""
## -------------------------------------------------------------------- ##
from pymatgen.io.vasp import Poscar
from ase.io import read, write
from ase.visualize import view
from pymatgen.io.vasp.sets import single_point

for i in range(len(all_slabs)):
    struct2 = Poscar(all_slabs[i])
    struct2.write_file('POSCAR')                                                # this poscar is different from the original one
    struct2_new = Structure.from_file('POSCAR')
    h = all_slabs[i].miller_index[0]
    k = all_slabs[i].miller_index[1]
    l = all_slabs[i].miller_index[2]
    dirname = 'slab_' + str(h) + str(k) + str(l)
    v = single_point(struct2_new)
    v.write_input(dirname)
## --------------------------------------------------------------------- ##

## What are the Miller indices of these slabs?
# for slab in all_slabs:
#     print slab.miller_index
