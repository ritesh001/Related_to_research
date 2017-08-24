#!/usr/bin/env python
"""Use for generating POSCARs and other input files from materials project"""
"""repsoitory using pymatgen"""

from pymatgen import MPRester
from pymatgen.io.vasp.sets import MPRelaxSet

m = MPRester("0LZXWNczpRl2CyOJ")
file1 = open('A2BO3F.dat','w')

data = m.query("*2*O3F",['material_id','pretty_formula','formation_energy_per_atom','spacegroup.symbol'])
###               ^                             ###
###               |                             ###
###   required formula of the structures        ###
###################################################

for i in range(len(data)):
        if data[i]['formation_energy_per_atom'] <= 0.2:
            f = 'POSCAR' + str(i) + '.vasp'
            g = 'POTCAR' + str(i)
            m_id = data[i]['material_id']
            # m_formula = data[i]['pretty_formula']
            # m_tot = m_formula + '_' + m_id
            structure = m.get_structure_by_material_id(m_id)
            v = MPRelaxSet(structure)
            v.write_input(m_id)
            file1.write('{:12} {:12} {:12.8f} {:12}\n'.format(data[i]['material_id'],data[i]['pretty_formula'],data[i]['formation_energy_per_atom'],data[i]['spacegroup.symbol']))
