#!/usr/bin/env python
"""Use it for calculating absorption coefficient from real and imaginary"""
"""parts of dielectric function"""

import numpy as np
import sys

f = open('abs-coeff.dat','w')                                                   # file in which absorption coefficient data is to be stored
hc = 1.2415e-6                                                                  # in eV

x1 = np.loadtxt('real.dat', usecols=[0]); y1 = np.loadtxt('real.dat', usecols=[1])
x2 = np.loadtxt('imag.dat', usecols=[0]); y2 = np.loadtxt('imag.dat', usecols=[1])

pre = (4.0 * np.pi * x1) / hc
pre1 = ((y1**2) + (y2**2)) ** (0.5)
alpha = pre * (((pre1 - y1) / 2) ** (0.5))                                      # in units of m^(-1)
alpha *= 1e-2                                                                   # in units of cm^(-1)
#x1 += float(sys.argv[4])                                                        # shifted by the shift in band gap

for i in range(len(alpha)):
    f.write("%f %f\n" %(x1[i], alpha[i]))
