#!/usr/bin/env python
from pymatgen import MPRester
from pymatgen.analysis.pourbaix_diagram import PourbaixDiagram, PourbaixPlotter
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry
mpr = MPRester('RfJHGVsqN8B0agKF')
#entries = mpr.get_pourbaix_entries(["Cu"])
#pbx = PourbaixDiagram(entries)
#entry = [e for e in entries if e.entry_id == 'mp-1692'][0]
#plotter = PourbaixPlotter(pbx)
#plotter.get_pourbaix_plot().show()
#print("CuO's potential energy per atom relative to the most",
#      "stable decomposition product is {:0.2f} eV/atom".format(
#          pbx.get_decomposition_energy(entry, pH=7, V=-0.2)))

comp = ['Ni2', 'H24O12', 'NiO', 'Ni4O8', 'NiH', 'NiO2H2']
ener = [-32.35063500, -195.38713000, -24.88995200, -124.59616000, -19.65337900, -41.10140500]
entry = [PDEntry(composition=comp[i], energy=ener[i]) for i in range(len(comp))]
pbx = PourbaixDiagram(entry)
plotter = PourbaixPlotter(pbx)
plotter.get_pourbaix_plot().show()
