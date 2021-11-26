# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:30:02 2020

@author: ritesh
"""

from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry
import numpy as np
import pandas as pd

two_d = pd.read_json('form-ener_scan_all_corr.json')
elem_no_t = two_d['Element_numbers']
elem_t = two_d['Elements']
comp_t = two_d['Compound']
ener_t = two_d['E_total']

bulk = pd.read_json('form-ener_scan_bulk_all_corr.json')
elem_no_b = bulk['Element_numbers']
elem_b = bulk['Elements']
comp_b = bulk['Compound']
ener_b = bulk['E_total']

## Generate unit cell formula of the compounds
def make_form(elem, elem_no):
    name = ''
    for i in range(len(elem)):
        name += elem[i] + str(elem_no[i])
    return name

## Check if formula of given 2D compound is a subset of the formula of any bulk material 
def check_elem_b(elem1):
    ind = []
    for i in range(len(elem_b)):
        A = elem1; B = elem_b[i]
        if set(B).issubset(set(A)) == True:
           ind.append(i)
    return ind

## Check if formula of given 2D compound is a subset of the formula of any other 2D material 
def check_elem_t(elem1):
    ind = []
    for i in range(len(elem_t)):
        A = elem1; B = elem_t[i]
        if set(B).issubset(set(A)) == True:
           ind.append(i)
    return ind


e_above_hull = []
#comp_or = comp_t[236:246]
df1 = pd.DataFrame()
#for j in range(236,246):
for j in range(len(comp_t)):
    #print(elem_t[j])
    print(comp_t[j])
    ind_b = check_elem_b(elem_t[j])
    ind_t = check_elem_t(elem_t[j])
    comp_n1 = [comp_b[ind_b[i]] for i in range(len(ind_b))]; comp_n2 = [comp_t[ind_t[i]] for i in range(len(ind_t))]
    comp_name = comp_n1 + comp_n2
    #print(comp_name)
    comp1 = [make_form(elem_b[ind_b[i]],elem_no_b[ind_b[i]]) for i in range(len(ind_b))]
    comp2 = [make_form(elem_t[ind_t[i]],elem_no_t[ind_t[i]]) for i in range(len(ind_t))]
    comp = comp1 + comp2
    #print(comp)
    ener1 = [ener_b[ind_b[i]] for i in range(len(ind_b))]; ener2 = [ener_t[ind_t[i]] for i in range(len(ind_t))]
    ener = ener1 + ener2
    #print(ener)
    ind = comp_name.index(comp_t[j])
    
    entry = [PDEntry(composition=comp[i], energy=ener[i]) for i in range(len(comp))]
    
    phd = PhaseDiagram(entry)
    for i in range(len(entry)):
        #print(comp[i], comp_name[i], phd.get_e_above_hull(entry[i]))
        info = {'2D': [comp_t[j]],
                'Compounds': [comp_name[i]],
                'E_above_hull': [phd.get_e_above_hull(entry[i])]}
        df1 = df1.append(pd.DataFrame(info))
        df2 = pd.DataFrame(df1, columns=['2D', 'Compounds', 'E_above_hull'])
    e_above_hull.append(phd.get_e_above_hull(entry[ind]))
    if sum(elem_no_t[j]) > 4:               ## since pymatgen does not support > 4-component convex hull figures
       continue
    else: 
       plotter = PDPlotter(phd, show_unstable=True)
       #plotter = PDPlotter(phd, show_unstable=True, backend='matplotlib')
       #plotter.show()
       f = comp_t[j] + '.png'
       plotter.write_image(f, image_format='png')

dict = {'Compound': comp_t, 'E_above_hull': e_above_hull}
df = pd.DataFrame(dict, columns=['Compound','E_above_hull'])
df.to_csv('hull-energy_scan_all.csv', index=False)
df2.to_csv('list_all-comp-hull.csv', index=False)
