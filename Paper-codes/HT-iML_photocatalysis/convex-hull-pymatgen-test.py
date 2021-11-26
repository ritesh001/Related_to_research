# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:03:43 2020

@author: ritesh
"""

from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry
import numpy as np

#comp = ['O', 'H', 'Ni', 'H2O', 'NiO', 'NiO2', 'NiH', 'NiO2H2']
comp = ['O8', 'H4', 'Ni2', 'H24O12', 'NiO', 'Ni4O8', 'NiH', 'NiO2H2']
ener = [-47.87163100, -16.34761600, -32.35063500, -195.38713000, -24.88995200, -124.59616000, -19.65337900, -41.10140500] ## scan energy
#ener = [-38.74762600, -13.30771500, -11.44176900, -178.01469000, -11.66778600, -66.63584600, -9.23737810, -25.80489000]  ## pbe energy
#ener_pa = np.array([0.000, 0.000, -0.657, -0.578, -0.570, -0.702])
n_atom = np.array([48, 1, 4, 10, 7, 6])
#ener = ener_pa * n_atom

entry = [PDEntry(composition=comp[i], energy=ener[i]) for i in range(len(comp))]

phd = PhaseDiagram(entry)
plotter = PDPlotter(phd, show_unstable=True)
plotter.show()
for i in range(len(entry)):
	print(comp[i], phd.get_e_above_hull(entry[i]))
