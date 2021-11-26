from warnings import filterwarnings
filterwarnings("ignore")
from pymatgen import Structure, Element
from pymatgen.io.vasp.inputs import Poscar

struc = Structure.from_file('CONTCAR')

sel = []
for i in range(len(struc)):
	# print(struc[i].specie)
	if struc[i].specie == Element('N') or struc[i].specie == Element('H'):
		sel.append([1, 1, 1])
	else:
		sel.append([0, 0, 0])

pos = Poscar(struc, selective_dynamics=sel)
pos.write_file('POSCAR')
