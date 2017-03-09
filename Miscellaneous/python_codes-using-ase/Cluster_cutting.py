from ase.io import read, write
from ase import Atoms
from ase.visualize import view
from ase.build import molecule

cluster = read('hcp.vasp')
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


pl = []                                          #different planes used in cutting the cluster
for i in range(10):
    for j in range(10):
        for k in range(10):
            a = [i,j,k]
            pl.append(a)

req = [[[],[]] for i in range(len(pl))]
div = [[[],[]] for i in range(len(pl))]
clusters = [[0,0] for j in range(len(pl))]

for p in pos:
    for i in range(len(pl)):
        b = plane(pl[i], p)
        if b <= 0:
            req[i][0].append(p)                                                 #all atoms lying on one side of plane made into new cluster#
        else:
            req[i][1].append(p)

for i in range(len(pl)):
    for j in range(2):
        q = len(req[i][j])
        if q == 27:
            l = i; m = j
            break
            #print i, j

n = abs(1-m)

##Writing POSCAR files of the two clusters cut##
cluster1 = Atoms('Pt27', req[l][m], cell=(28,28,28))
write("h1.vasp", cluster1)
#view(cluster1)
cluster2 = Atoms('Pt28', req[l][n], cell=(28,28,28))
write("h2.vasp", cluster2)
#view(cluster2)
print "The plane used for cutting is %s\n" % (pl[l])
