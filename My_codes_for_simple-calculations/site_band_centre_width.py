#!/usr/bin/env python
"""script for calculating d-band (or other band) center and width for a specific site"""
"""This script is for slab type of structures, where dbc and dbw are calculated only for surface atoms"""

import warnings
warnings.filterwarnings('ignore')
from pymatgen.io.vasp import Vasprun   
from pymatgen.electronic_structure.core import Spin
from collections import namedtuple
from ase.dft import get_distribution_moment
import sys

## total dos and total d-band centre
dosrun = Vasprun("vasprun.xml")
dos = dosrun.complete_dos
spd_dos = dosrun.complete_dos.get_spd_dos()
d_named = namedtuple('Struct', spd_dos.keys())(*spd_dos.values())              # Arun's contribution; don't understand :-(
if sys.argv == 'up':
	d_orb = d_named.d.densities[Spin.up]
else:
	d_orb = d_named.d.densities[Spin.down]
x = dosrun.tdos.energies - dosrun.efermi

dbc = get_distribution_moment(x, d_orb, order=1)
dbw = get_distribution_moment(x, d_orb, order=2)

print "d-band center of system (%s) = %f eV" %( sys.argv[1], dbc)
print "d-band width of system (%s) = %f eV" %( sys.argv[1], dbw)

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

## site dos and site d-band centre
f = open('d-band-%s_centre_width.dat' %(sys.argv[1]), 'w')
for site in sites:
	# if struc.site_properties['selective_dynamics'][i][0] == True:
	site_dos = dos.get_site_spd_dos(dos.structure[site])
	site_d_named = namedtuple('Struct', site_dos.keys())(*site_dos.values())
	if sys.argv[1] == 'up':
		site_d_orb = site_d_named.d.densities[Spin.up]
	else:
		site_d_orb = site_d_named.d.densities[Spin.down]
	dbc_site = get_distribution_moment(x, site_d_orb, order=1)
	dbw_site = get_distribution_moment(x, site_d_orb, order=2)
	el = str(struc[site].specie)
	if el in atoms:
		n = atoms.index(el)
		z = 0
		for k in range(n):
			z += atoms_number[k]
	r = (site + 1) - z
	f.write("%6s %6.2f %6.2f\n" %(el + '-' + str(r),dbc_site,dbw_site))

f.close()

