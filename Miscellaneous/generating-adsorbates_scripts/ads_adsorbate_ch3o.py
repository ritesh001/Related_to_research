import warnings, sys, os
warnings.filterwarnings('ignore')
from pymatgen import Structure, Lattice, MPRester, Molecule
from pymatgen.analysis.adsorption import *
from pymatgen.core.surface import generate_all_slabs
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from matplotlib import pyplot as plt
from ase.build import molecule
from shutil import copyfile
from ase.io import read, write

curr_dir = os.getcwd()

a = Structure.from_file('POSCAR')
b = AdsorbateSiteFinder(a)
ads_sites = b.find_adsorption_sites()
#adsorbate = Molecule("COO", co2_pos)
ch3o = read('ch3o.vasp')
#ch3o.rotate(50.7685,'z')
ch3o.rotate(90,'x')
ch3o_pos = ch3o.get_positions()
adsorbate = Molecule("COHHH", ch3o_pos)
ads_structs = b.generate_adsorption_structures(adsorbate)
#print len(ads_structs)
for i in range(len(ads_structs)):
        #path = curr_dir + '/' + str(i)
        #os.makedirs(path)
        #os.chdir(path)
        #f = 'POSCAR'
        f = 'POSCAR_' + str(i) + '.vasp' 
        ads_structs[i].to(filename=f)
        #copyfile(curr_dir + '/' + 'INCAR' , path + '/' + 'INCAR')
        #copyfile(curr_dir + '/' + 'KPOINTS' , path + '/' + 'KPOINTS')
        #copyfile(curr_dir + '/' + 'POTCAR' , path + '/' + 'POTCAR')
        #os.chdir(curr_dir)
