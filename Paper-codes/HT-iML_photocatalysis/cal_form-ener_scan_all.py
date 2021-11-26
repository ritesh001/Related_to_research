import os, sys
import numpy as np
import pandas as pd
from pymatgen import Structure
from ase.io import read

images = []
curr_dir = os.getcwd()

list = pd.read_csv('all-list_comp.csv')
a = list['Compound']

def read_poscar(file):
	f0 = open('POSCAR','r')
	b = []
	for line in f0:
		a = line.split()
		a = [a[i] for i in range(len(a))]
		b.append(a)
	f0.close()
	atoms = []
	atoms_number = []
	for j in range(len(b[5])):
		atoms.append(b[5][j])
		atoms_number.append(int(b[6][j]))
	return atoms, atoms_number

ref = pd.read_csv('all-ref_scan.csv')    ## need this file also
def sum_ref_energies(sym, number):
	s = 0
	for i in range(len(sym)):
		s += number[i] * float(ref[ref['Element'] == sym[i]]['Energy/atom'])
	return s
		
comp = []; elem = []; elem_num = []; total_en = []; form_en = []; num = []
for i in range(len(a)):
    path = curr_dir + '/' + a[i]
    comp.append(a[i])        ## uncomment when list contains '/' at the end
    os.chdir(path)
    print(path)
    sym, number = read_poscar('POSCAR')
    elem.append(sym); elem_num.append(number)
    num.append(sum(number))
    out = read('OUTCAR')
    tot_energy = out.get_total_energy()
    total_en.append(tot_energy)
    ref_tot = sum_ref_energies(sym, number)
    formation_energy = tot_energy - ref_tot
    formation_energy /= sum(number)
    form_en.append(formation_energy)
    os.chdir(curr_dir)
	
dict = {'Compound': comp, 'Elements': elem, 'Element_numbers': elem_num,
        'H_f': form_en, 'E_total': total_en, '#_atoms': num}
df = pd.DataFrame(dict, columns=['Compound','Elements','Element_numbers',
                 'H_f','E_total','#_atoms'])
file_name_csv = 'form-ener_scan_all'  + '.csv'
file_name_json = 'form-ener_scan_all'  + '.json'
df.to_csv(file_name_csv, index=False)
df.to_json(file_name_json)
