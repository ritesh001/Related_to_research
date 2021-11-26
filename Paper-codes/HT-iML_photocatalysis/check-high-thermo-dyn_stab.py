# -*- coding: utf-8 -*-
"""
Created on Sat Nov 7 2020

@author: ritesh
"""

f3 = open('high-thermo_dyn-done.txt','w')

with open('high-thermo_dyn-list.txt','r') as f1:
	a1 = f1.readlines()
comp1 = [a1[i].split()[0] for i in range(len(a1))]

with open('done','r') as f2:
	a2 = f2.readlines()
comp2 = [a2[i].split()[0] for i in range(len(a2))]

# print(comp2)
for i in range(len(comp1)):
	if comp1[i] in comp2:
		print(comp1[i])
		f3.write('%s\n' %(comp1[i]))

f1.close(); f2.close(); f3.close()