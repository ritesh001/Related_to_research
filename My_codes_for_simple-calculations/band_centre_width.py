from pymatgen.io.vasp import Vasprun   
from pymatgen.electronic_structure.core import Spin
from collections import namedtuple
from ase.dft import get_distribution_moment
import sys

"""script for calculating d-band centre and width"""
"""use it as : python band_centre_width.py"""

dosrun = Vasprun("vasprun.xml")
dos = dosrun.complete_dos
spd_dos = dosrun.complete_dos.get_spd_dos()
d_named = namedtuple('Struct', spd_dos.keys())(*spd_dos.values())
d_orb = d_named.d.densities[Spin.up]
x = dosrun.tdos.energies - dosrun.efermi

dbc = get_distribution_moment(x, d_orb, order=1)
dbw = get_distribution_moment(x, d_orb, order=2)

print "d-band center of system = %f eV" %(dbc)
print "d-band width of system = %f eV" %(dbw)

set = dos.structure.symbol_set
elements_present = [set[i] for i in range(len(set))]

for element in elements_present:
	e_spd_dos = dos.get_element_spd_dos(element)                                           # change to required element
	e_d_named = namedtuple('Struct', e_spd_dos.keys())(*e_spd_dos.values())
	e_d_orb=e_d_named.d.densities[Spin.up]                                                   # change to 's' or 'p' for the respective orbitals

	print "------ %s -------" %(element)
	dbce = get_distribution_moment(x, e_d_orb, order=1)
	print "d-band center = %f eV" %(dbce)
	dbwe = get_distribution_moment(x, e_d_orb, order=2)
	print "d-band width = %f eV" %(dbwe)

