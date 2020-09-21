# from pymatgen.matproj.rest import MPRester
from pymatgen import MPRester

m = MPRester("0LZXWNczpRl2CyOJ")
file1 = open('list.dat','w')

# data = m.query(criteria={"elements": {"$in":["La","Mn","Fe"],"$all":["O"]},"nelements":3}, properties=["material_id","formation_energy_per_atom"])
data = m.query(criteria={"elements": {"$in":["Ti","V","Cr","Mn","Fe"],"$in":["La"],"$all":["O"]},"nelements":3}, properties=["material_id","formation_energy_per_atom","spacegroup.symbol","formula"])
# data = m.query(criteria={"elements": {"$in":["Li","Na","Ka"],"$all":["O"]},"nelements":2}, properties=["material_id","formation_energy_per_atom"])

for i in range(len(data)):
    if data[i]['spacegroup.symbol'] == 'Pm-3m':
        if data[i]['formation_energy_per_atom'] <= 0.2:
            f = 'POSCAR' + str(i) + '.vasp'
            structure = m.get_structure_by_material_id(data[i]['material_id'])
            structure.to(fmt='poscar')
            structure.to(filename=f)
            file1.write('{:12} {:12} {:8}\n'.format(data[i]['material_id'],data[i]['formation_energy_per_atom'],data[i]['spacegroup.symbol']))
