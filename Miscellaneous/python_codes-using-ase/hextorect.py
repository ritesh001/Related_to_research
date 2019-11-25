from __future__ import print_function
#get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import math
from ase.io.vasp import read_vasp
from ase.build import make_supercell
from ase.build import cut
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from ase.io import read, write
mpl.rc('font',**{'size' : 13})

cell = read_vasp("POSCAR")   # reading the poscar file
cell1=cell.get_cell()     # not needed really
cell1[2][2] = 18.0
atoms=make_supercell(cell,[[3,0,0],[0,3,0],[0,0,1]])    # make supercell of the poscar file
print (type(atoms))       # to check  the presence of atoms   returns none if no atoms detected  
cellnew=atoms.get_cell()   # new cell is created for the supercell
cellnew[1,0]=0              # make the supercell straight   but beware the cell is destroyed after some distance
cellnew[2][2] = 18.0
atoms.set_cell(cellnew)      # 
atoms.center()
atoms.wrap()

# Creation of orthorhombic cell by cutting the supercell created
atomnew=cut(atoms, a=(1/3,0,0), b=(0,2/3,0), c=(0,0,1), clength=None, origo=(0, 0, 0), nlayers=None, extend=1.0, tolerance=0.01) 

#  Check presence of atoms ```

cellfin=atomnew.get_cell()
print (type(cellfin))
print (cellfin)


# Write final POSCAR file

atomnew.write("CONTCAR")
#write(atomnew, 'CONTCAR')
