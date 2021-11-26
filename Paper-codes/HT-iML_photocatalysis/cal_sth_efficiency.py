#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 14:19:36 2021

@author: ritesh
"""

import pandas as pd
from scipy import interpolate
from scipy.integrate import trapz
import numpy as np
import sys


df1 = pd.read_csv('elec-struc_gw_pbe_htd.csv')
comp = df1['Compound']
bandgap = df1['Bandgap_GW']
del_phi_list = df1['diff_vac_lev']
chi_h2_list = df1['chi_H2']
chi_o2_list = df1['chi_O2']
oer_list = df1['OER']
her_list = df1['HER']

#### Calculating eta_STH
data = pd.read_excel('am15g_mod.xls', sheet_name='data')
x = data['E_eV']
# y = data['direct_eV']
y = data['glob_eV']
y_ = y/x

eta_STH_list = []
""" 
Formula:
eta_STH = (del_G * I_1) / (I_2 + (del_phi * I_3))
"""
# =============================================================================
# For I_2  
# =============================================================================
I_2 = trapz(y, x, dx=0.1)
# print(I_2)

for i in range(len(comp)):
    print(comp[i])
    chi_h2 = chi_h2_list[i]
    chi_o2 = chi_o2_list[i]
    del_phi = abs(del_phi_list[i])
    Eg = bandgap[i]
    
    if chi_h2 >= 0.2 and chi_o2 >= 0.6:
        E = Eg
    elif chi_h2 < 0.2 and chi_o2 >= 0.6:
        E = Eg + 0.2 - chi_h2
    elif chi_h2 >= 0.2 and chi_o2 < 0.6:
        E = Eg + 0.6 - chi_o2
    elif chi_h2 < 0.2 and chi_o2 < 0.6:
        E = Eg + 0.8 - chi_h2 - chi_o2
        
    # print(E)
    h = 6.626e-34              # units of J s
    c = 3e8                    # units of m s-1
    
    def find_nearest_num(n):
        check = []
        for i in range(len(x)):
            check.append(abs(x[i] - n))
        ind = check.index(min(check))
        return x[ind], ind
    
    # =============================================================================
    # For I_1
    # =============================================================================
    lower_limit_1, ind_1 = find_nearest_num(E)
    # print(lower_limit_1)
    x_1 = x[ind_1:]; y_1 = y_[ind_1:]
    I_1 = trapz(y_1, x_1, dx=0.1)
    # print(I_1)
    # -----------------------------------------------------------------------------
    
    # =============================================================================
    # For I_3
    # =============================================================================
    lower_limit_3, ind_3 = find_nearest_num(Eg)
    # print(lower_limit_3)
    x_3 = x[ind_3:]; y_3 = y_[ind_3:]
    I_3 = trapz(y_3, x_3, dx=0.1)
    # print(I_3)
    
    del_G = 1.23
    
    eta_STH = (del_G * I_1) / (I_2 + (del_phi * I_3))
    eta_STH *= 100
    eta_STH_list.append(eta_STH)
    print(eta_STH)
    # -----------------------------------------------------------------------------

dict = {'Compound': comp, 'bandgap': bandgap, 'del_phi': del_phi_list,
        'chi_H2': chi_h2_list, 'chi_O2': chi_o2_list, 'OER': oer_list,
        'HER': her_list, 'eta_STH': eta_STH_list}
df2 = pd.DataFrame(dict, columns=['Compound', 'bandgap', 'del_phi', 'chi_H2', 'chi_O2',
                                  'OER', 'HER', 'eta_STH'])
df2.to_csv('opt_band_sth.csv', index=False)