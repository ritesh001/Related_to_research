from pymatgen.io.vasp import Vasprun
dosrun = Vasprun("vasprun.xml")
a = dosrun.get_band_structure() 
b = a.get_band_gap() 
print b['energy']
