#!/usr/bin/env python

import warnings
warnings.filterwarnings("ignore")
from pymatgen import Element
from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.io.vasp import Structure
import os
from ase import Atoms
from ase.io import read, write

curr_dir = os.getcwd()
iii_y_dir = curr_dir + '/../M_iii_OH-Y'

func_group_ii = ['O', 'S', 'Se', 'Te', 'NH', 'PH']
cl = Atoms('Cl')
br = Atoms('Br')
iod = Atoms('I')
fl = Atoms('F')
cn = Atoms('CN',([0,0,0],[0,0,1.13]))
nc = Atoms('NC',([0,0,0],[0,0,1.13]))
no = Atoms('NO',([0,0,0],[0,0,1.136]))
sh = Atoms('SH',([0,0,0],[0,0,0.98]))
nco = Atoms('NCO',([0,0,0],[0,0,1.22],[0,0,2.78]))
ncs = Atoms('NCS',([0,0,0],[0,0,1.22],[0,0,2.78]))
ocn = Atoms('OCN',([0,0,0],[0,0,1.65],[0,0,2.82]))
scn = Atoms('SCN',([0,0,0],[0,0,1.65],[0,0,2.82]))
func_group_i = [cl,br,iod,fl,cn,nc,nco,ncs,no,ocn,scn,sh]
func_group_i_str = ['Cl','Br','I','F','CN','NC','NCO','NCS','NO','OCN','SCN','SH']
dop = ['Al', 'Ga', 'In', 'Ru', 'Y', 'La', 'Bi','Rh', 'Cr', 'Sc','Ce', 'Co', 'Fe', 'Gd', 'Ir', 'Lu', 'Nd', 'Sm']

def find_o_site(struc):
	c = []
	for i in range(len(struc)):
		a = struc[i].specie
		b = str(a)
		if b in 'O':
			c.append(i)
	if len(c) > 1:
		d = c[0]; e = c[1]
		coor1 = struc[d].coords[2]; coor2 = struc[e].coords[2]
		if coor1 > coor2:
			x = d
		elif coor1 < coor2:
			x = e
	elif len(c) == 1:
		x = c[0]
	return x

def del_h_site(struc):
	c = []
	for i in range(len(struc)):
		a = struc[i].specie
		b = str(a)
		if b in 'H':
			c.append(i)
	if len(c) > 1:
		d = c[0]; e = c[1]
		coor1 = struc[d].coords[2]; coor2 = struc[e].coords[2]
		if coor1 > coor2:
			x = d
		elif coor1 < coor2:
			x = e
	elif len(c) == 1:
		x = c[0]
	del struc[x]

def replace_o_site(b):          ## b = ith element of func_group_i
	a = find_o_site(struc)
	pos = b.get_positions()
	sym = b.get_chemical_symbols()
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

for i in range(len(func_group_ii)):
	fun_dir = iii_y_dir + '/' + func_group_ii[i]
	for dopants in dop:
		dop_dir = fun_dir + '/' + dopants + '/latt-opt'
		os.chdir(dop_dir)
                struc_ase = read('CONTCAR')
                cell = struc_ase.cell
                cell[2][2] = 20.0
                write('CONTCAR',struc_ase)
		struc = Structure.from_file('CONTCAR')
		for j in range(len(func_group_i)):
			fin_dir = curr_dir + '/' + func_group_ii[i] + '-' + func_group_i_str[j] + '-' + dopants
			os.makedirs(fin_dir)
			os.chdir(fin_dir)
			del_h_site(struc)
			replace_o_site(func_group_i[j])
			v = MPRelaxSet(struc)
			v.write_input('./latt-opt')
			os.chdir(dop_dir)
			struc = Structure.from_file('CONTCAR')
