#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore")
from pymatgen import Element
from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.io.vasp import Structure
import os, shutil
from ase import Atoms

curr_dir = os.getcwd()

cl = Atoms('Cl')
br = Atoms('Br')
iod = Atoms('I')
fl = Atoms('F')
cn = Atoms('CN',([0,0,0],[0,0,1.13]))
nc = Atoms('NC',([0,0,0],[0,0,1.13]))
no = Atoms('NO',([0,0,0],[0,0,1.136]))
sh = Atoms('SH',([0,0,0],[0,0,0.98]))
oh = Atoms('OH',([0,0,0],[0,0,0.98]))
nco = Atoms('NCO',([0,0,0],[0,0,1.22],[0,0,2.78]))
ncs = Atoms('NCS',([0,0,0],[0,0,1.22],[0,0,2.78]))
ocn = Atoms('OCN',([0,0,0],[0,0,1.65],[0,0,2.82]))
scn = Atoms('SCN',([0,0,0],[0,0,1.65],[0,0,2.82]))
func_group_i = [cl,iod,fl,cn,nc,nco,ncs,no,ocn,scn,sh, oh]
func_group_i_str = ['Cl','I','F','CN','NC','NCO','NCS','NO','OCN','SCN','SH', 'OH']
dop = ['Be','Mg','Ca','Sr','Ba','Mn','Fe','Co','Ni','Cu','Zn','Cd','Pd','Pt','Pb']

def find_u_site(struc):
	coor = []
	for i in range(len(struc)):
		coor.append(struc[i].coords[2])
		m = max(coor)
	return coor.index(m)

def replace_u_site(b):          ## b = ith element of func_group_i
	pos = b.get_positions()
	sym = b.get_chemical_symbols()
	a = find_u_site(struc)
	if len(b) == 1:
		struc.replace(a, Element(sym[0]))
	elif len(b) == 2:
		struc.replace(a, Element(sym[0]))
		func_atom_coor = [0,0,0]
		for i in range(2):
			func_atom_coor[i] = struc[a].coords[i] - pos[1][i]
		func_atom_coor[2] = struc[a].coords[2] + pos[1][2]
		struc.append(sym[1], func_atom_coor, coords_are_cartesian=True)
	elif len(b) == 3:
		struc.replace(a, Element(sym[0]))
		func_atom_coor1 = [0,0,0]; func_atom_coor2 = [0,0,0]
		for i in range(2):
			func_atom_coor1[i] = struc[a].coords[i] - pos[1][i]
			func_atom_coor2[i] = struc[a].coords[i] - pos[2][i]
		func_atom_coor1[2] = struc[a].coords[2] + pos[1][2]
		func_atom_coor2[2] = struc[a].coords[2] + pos[2][2]
		struc.append(sym[1], func_atom_coor1, coords_are_cartesian=True)
		struc.append(sym[2], func_atom_coor2, coords_are_cartesian=True)
	return struc

for dopants in dop:
	dop_dir = curr_dir + '/' + dopants + '/relax'
	dop_dir_1 = curr_dir + '/' + dopants
	print dop_dir
	os.chdir(dop_dir)
	struc = Structure.from_file('CONTCAR')
	# print struc
	for i in range(len(func_group_i)):
		# print find_u_site(struc)
		replace_u_site(func_group_i[i])
		dir_name = func_group_i_str[i] + '-' + 'Br-' + dopants
		new_dir = curr_dir + '/' + dir_name + '/latt-opt'
		v = MPRelaxSet(struc)
		v.write_input(new_dir)
		struc = Structure.from_file('CONTCAR')
	shutil.rmtree(dop_dir_1)