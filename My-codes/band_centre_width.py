#!/usr/bin/env python
"""script for calculating band center and width for a specific site"""
"""Usage : python band_centre_width.py <all or sur or specified sites separated by comma> <up or down>"""

import warnings
warnings.filterwarnings('ignore')
from pymatgen.io.vasp import Vasprun   
from pymatgen.electronic_structure.core import Spin
from collections import namedtuple
from ase.dft import get_distribution_moment
import sys

dosrun = Vasprun("vasprun.xml")
dos = dosrun.complete_dos
x = dosrun.tdos.energies - dosrun.efermi

## atom numbers from POSCAR
f0 = open("POSCAR","r")
b = []
for line in f0:
    a = line.split()
    a = [a[i] for i in range(len(a))]
    b.append(a)
f0.close()

atoms = []
atoms_number = []
for j in range(len(b[5])):
    atoms.append(b[5][j])
    atoms_number.append(int(b[6][j]))

## finding indices of surface atoms
struc = dos.structure

if sys.argv[1] == 'sur':
	z_coor = []; sites = []
	for i in range(len(struc)):
		z_coor.append(int(struc[i].coords[2]))
	for j in range(len(z_coor)):
		if z_coor[j] == max(z_coor):
			sites.append(j)
		elif z_coor[j] == max(z_coor) - 1:
			sites.append(j)
		else:
			continue
elif sys.argv[1] == 'all':
	sites = [i for i in range(len(struc))]

## site dos and site band centre
f = open('band-%s_centre_width.dat' %(sys.argv[2]), 'w')
for site in sites:
	# if struc.site_properties['selective_dynamics'][i][0] == True:
	site_dos = dos.get_site_spd_dos(dos.structure[site])
	site_named = namedtuple('Struct', site_dos.keys())(*site_dos.values())
	el = struc[site].specie
	if sys.argv[1] == 'up':
		site_s_orb = site_named.s.densities[Spin.up]
		if el.block == 'p':
			site_p_orb = site_named.p.densities[Spin.up]
			site_d_orb = [0 for i in range(len(x))]
			site_f_orb = [0 for i in range(len(x))]
		elif el.block == 'd':
			site_p_orb = site_named.p.densities[Spin.up]
			site_d_orb = site_named.d.densities[Spin.up]
			site_f_orb = [0 for i in range(len(x))]
		elif el.block == 'f':
			site_p_orb = site_named.p.densities[Spin.up]
			site_d_orb = site_named.d.densities[Spin.up]
			site_f_orb = site_named.f.densities[Spin.up]
	else:
		site_s_orb = site_named.s.densities[Spin.down]
		if el.block == 'p':
			site_p_orb = site_named.p.densities[Spin.down]
			site_d_orb = [0 for i in range(len(x))]
			site_f_orb = [0 for i in range(len(x))]
		elif el.block == 'd':
			site_p_orb = site_named.p.densities[Spin.down]
			site_d_orb = site_named.d.densities[Spin.down]
			site_f_orb = [0 for i in range(len(x))]
		elif el.block == 'f':
			site_p_orb = site_named.p.densities[Spin.down]
			site_d_orb = site_named.d.densities[Spin.down]
			site_f_orb = site_named.f.densities[Spin.down]

	sbc_site = get_distribution_moment(x, site_s_orb, order=1); sbw_site = get_distribution_moment(x, site_s_orb, order=2)
	pbc_site = get_distribution_moment(x, site_p_orb, order=1); pbw_site = get_distribution_moment(x, site_p_orb, order=2)
	dbc_site = get_distribution_moment(x, site_d_orb, order=1); dbw_site = get_distribution_moment(x, site_d_orb, order=2)
	fbc_site = get_distribution_moment(x, site_f_orb, order=1); fbw_site = get_distribution_moment(x, site_f_orb, order=2)
	el = str(el)
	if el in atoms:
		n = atoms.index(el)
		z = 0
		for k in range(n):
			z += atoms_number[k]
	r = (site + 1) - z
	f.write("%6s %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f\n" %(el + '-' + str(r),sbc_site,sbw_site,pbc_site,pbw_site,
	dbc_site,dbw_site,fbc_site,fbw_site))

f.close()

