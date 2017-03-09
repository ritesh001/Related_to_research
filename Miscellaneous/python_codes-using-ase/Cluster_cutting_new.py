from ase.io import read, write
from ase import Atoms
from ase.visualize import view
from ase.build import molecule
from random import randint as rnd

cluster = read('icosahedron.vasp')
#view(cluster)

COM = cluster.get_center_of_mass()                                              #center of mass

pos = cluster.positions                                                         #positions of atoms of the cluster

##function for determining whether atom lies on plane, or right or left of plane##
def plane(pl, p):                                                               #pl = plane; p = position of atom
    s = 0
    for i in range(3):
        a = p[i] - COM[i]
        a *= pl[i]
        s += a                                                                  #if s=0 then lies on plane, if s > 0 then lies on one side of the plane and if s < 0#
    return s                                                                    #then lies on another side of the plane#



req = [[],[]]
while True:
    pl = [(rnd(0,9)),(rnd(0,9)),(rnd(0,9))]
    for p in pos:
        b = plane(pl, p)
        if b <= 0:
            req[0].append(p)                                                    #all atoms lying on one side of plane made into new cluster#
        else:
            req[1].append(p)
    l = len(req[0])
    if l == 27 or l == 28:
        m = l
        break
    req = [[],[]]

n = str(abs(55-m)); m = str(m)
c1 = 'Pt' + m
c2 = 'Pt' + n
##Writing POSCAR files of the two clusters cut##
cluster1 = Atoms(c1, req[0], cell=(28,28,28))
write("ico1.vasp", cluster1)
#view(cluster1)
cluster2 = Atoms(c2, req[1], cell=(28,28,28))
write("ico2.vasp", cluster2)
# #view(cluster2)
print "The plane used for cutting is %s\n" % (pl)
