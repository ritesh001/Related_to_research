from ase.io import read, write
from ase import Atoms
from ase.visualize import view
import random as rn
from random import randint as rnd
import math
import numpy as np

cluster = read('icosahedron.vasp')
#view(cluster)

##Center of mass##
COM = cluster.get_center_of_mass()

##Positions of atoms of the cluster##
pos = cluster.positions

##Function for determining whether atom lies on plane, or right or left of plane##
def plane(pl, p):
    """pl = plane; p = position of atom"""
    s = 0
    for i in range(3):
        a = p[i] - COM[i]
        a *= pl[i]
        s += a
    """if s=0 then lies on plane, if s > 0 then lies on one side of the plane"""
    """and if s < 0 then lies on another side of the plane"""
    return s

##Function for calculating distance of a point from a plane##
##and then store the points in an array according to increasing distance##
def dist(arr,pl):
    a=pl[0]; b=pl[1]; c=pl[2]
    dst=[]; temp_arr=[]
    den = math.sqrt(a**2+b**2+c**2)
    tmp = arr
    l=len(tmp)
    for i in range (0,l):
        d = tmp[i][0]*a+tmp[i][1]*b+tmp[i][2]*c-(a*COM[0]+b*COM[1]+c*COM[2])
        d /= den
        dst.append(d)
    """Bubble sorting"""
    for i in range (0,l):
        for j in range (i+1,l):
            if dst[i] > dst [j] :
                temp = dst[i]
                dst[i] = dst[j]
                dst[j] = temp
                temp_arr = tmp[i]
                tmp[i] = tmp[j]
                tmp[j] = temp_arr
    return tmp

req = [[],[]]

##Random a,b,c for the plane##
a = np.array([(rnd(0,9)),rnd(0,9),rnd(0,9)]) + np.array([rn.random(),rn.random(),rn.random()])
b = np.array([rn.random(),rn.random(),rn.random()])
c = np.array([(rnd(0,9)),rnd(0,9),rnd(0,9)])
d = rn.random()
if d < 0.33:
    pl = a
elif d > 0.33 and d < 0.66:
    pl = b
else:
    pl = c

##Splitting the cluster into two##
for p in pos:
    b = plane(pl, p)
    if b <= 0:
        req[0].append(p)
    else:
        req[1].append(p)
    """all atoms lying on one side of plane split into one half"""
l = len(req[0])
if l != 27 or l != 28:
    """Add atoms to req[0]"""
    if l<27:
        temp=[]
        temp=dist(req[1],pl)
        j=0
        while l!=27 or l!=28 :
            req[0].append(temp[j])
            req[1].remove(temp[j])
            l+=1
            j+=1
    """Remove atoms from req[0]"""
    if l>28 :
        temp=[]
        temp=dist(req[0],pl)
        i=0
        while l!=27 or l!=28 :
            req[1].append(temp[i])
            req[0].remove(temp[i])
            i+=1
            l-=1
#print l

m = l; n = str(abs(55-m)); m = str(m)
c1 = 'Pt' + m; c2 = 'Pt' + n

##Writing POSCAR files of the two split clusters##
cluster1 = Atoms(c1, req[0], cell=(28,28,28))
write("ico1.vasp", cluster1)
#view(cluster1)
cluster2 = Atoms(c2, req[1], cell=(28,28,28))
write("ico2.vasp", cluster2)
#view(cluster2)
print "The plane used for cutting is %s\n" % (pl)
