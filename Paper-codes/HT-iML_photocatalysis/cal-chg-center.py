from ase.calculators.vasp.vasp import VaspChargeDensity
from ase.io import read
import numpy as np

atoms = read('POSCAR')
#cell = struc.cell

def get_charge_density(filename="CHGCAR"):
    vd = VaspChargeDensity(filename)

    data = np.array(vd.chg)
    n0, n1, n2 = data[0].shape

    s0 = 1.0 / n0
    s1 = 1.0 / n1
    s2 = 1.0 / n2
    X, Y, Z = np.mgrid[0.0:1.0:s0,
                       0.0:1.0:s1,
                       0.0:1.0:s2]

    C = np.column_stack([X.ravel(),
                         Y.ravel(),
                         Z.ravel()])

    uc = atoms.get_cell()
    real = np.dot(C, uc)

    # now convert arrays back to unitcell shape
    x = np.reshape(real[:, 0], (n0, n1, n2))
    y = np.reshape(real[:, 1], (n0, n1, n2))
    z = np.reshape(real[:, 2], (n0, n1, n2))
    return (x, y, z, data[0])

x, y, z, cd = get_charge_density()
#print(cd.shape)
n0, n1, n2 = cd.shape
nelements = n0 * n1 * n2
voxel_volume = atoms.get_volume() / nelements
total_electron_charge = cd.sum() * voxel_volume
#print ("total electrons =", total_electron_charge)
#print(x)
#print(len(x))

electron_density_center = np.array([(cd * x).sum(),
                                    (cd * y).sum(),
                                    (cd * z).sum()])
electron_density_center *= voxel_volume
electron_density_center /= total_electron_charge
#print("electron density center =", electron_density_center)

uc = atoms.get_cell()
sedc = np.dot(np.linalg.inv(uc.T), electron_density_center.T).T
sedc = np.round(sedc, 4)
print(sedc[0], sedc[1], sedc[2])
