#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:14:54 2020

@author: thsim7
"""

import matplotlib.pyplot as plt
import pandas as pd
#from sklearn import metrics

data = pd.read_csv('free-H_icohp.csv')
#data = pd.read_csv('ads-ener_H_icohp.csv')

x = data['ICOHP']
y = data['del_G_H']
#y = data['del_E_H']

#marker_list = ['o','v','^','>','<','*','s','D','P','X','h','H','8']
#for i in range(len(data)):
#    plt.plot(x[i], y[i], c='cyan', marker=marker_list[i], markeredgecolor='b', 
#             label=data['M'][i], markersize=10)
##plt.text(0.5, 0.1, '$R^2$:  {:.2f}'.format(r2))

#fig, ax = plt.subplots()
plt.scatter(x, y, c='cyan', marker='o', s=100, edgecolors='b')

#for i, txt in enumerate(data['M']):
#    plt.annotate(txt, (x[i], y[i]))
#plt.legend()
plt.show()