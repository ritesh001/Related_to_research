from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.core import Spin

dosrun = Vasprun("vasprun.xml")
dos = dosrun.complete_dos
y = dos.get_densities()
x = x = dosrun.tdos.energies - dosrun.efermi
y1 = dos.densities[Spin.up]
y2 = dos.densities[Spin.down]

f1 = open('tdos_up.dat', 'w')
f2 = open('tdos_down.dat', 'w')

for i in range(len(x)):
	f1.write('{0:10.3f} {1:10.3f}\n'.format(x[i], y1[i]))
	f2.write('{0:10.3f} {1:10.3f}\n'.format(x[i], -y2[i]))

f1.close()
f2.close()