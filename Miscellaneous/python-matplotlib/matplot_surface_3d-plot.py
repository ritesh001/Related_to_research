import numpy as np
import matplotlib.pylab as p
from mpl_toolkits.mplot3d import Axes3D

kx = p.arange(-2, 2 , 0.01)
ky = p.arange(-2, 2 , 0.01)
X, Y = p.meshgrid(kx, ky)

a = 2.46
gamma = -2.7
b = (p.sqrt(3)*a)/2.0; c = a / 2.0

mod_fk_sq = 1 + (4 * p.cos(b * X) * p.cos(c * Y)) + (4 * (p.cos(c * Y))**2)
E1 = gamma * p.sqrt(mod_fk_sq)
E2 = -E1

fig = p.figure()
ax = Axes3D(fig)
ax.plot_surface(X, Y, E1)
ax.plot_surface(X, Y, E2)
ax.set_xlabel('kx'); ax.set_ylabel('ky'); ax.set_zlabel('Energy (eV)')
ax.xaxis.label.set_color('red'); ax.yaxis.label.set_color('green'); ax.zaxis.label.set_color('blue')
ax.set_title('Prob 1.ii.a : Only nearest neighbour contribution')
ax.view_init(20,-120)

p.show()
