#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pyplot as plt

f = np.genfromtxt(sys.argv[1])
#print(f)
print(len(f))

f_t = f.transpose()
time = f_t[1]
pot_ener = f_t[4]
tot_ener = f_t[5]

#plt.plot(time, pot_ener, label='Potential energy')
plt.plot(time, tot_ener, label='Total energy')
plt.legend()
plt.xlabel('Time (fs)')
plt.ylabel('Energy (eV)')
plt.show()
