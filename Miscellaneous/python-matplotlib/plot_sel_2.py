#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:14:54 2020

@author: thsim7
"""

import matplotlib.pyplot as plt
import pandas as pd
#from sklearn import metrics

data = pd.read_csv('selectivity.csv')

x = data['del_H']
y = data['del_N2H']

marker_list = ['o','v','^','>','<','*','s','D','P','X','h','H','8']
for i in range(len(data)):
    plt.plot(x[i], y[i], c='cyan', marker=marker_list[i], markersize='10', 
			 markeredgecolor='b', label=data['M'][i])
#plt.text(0.5, 0.1, '$R^2$:  {:.2f}'.format(r2))
plt.legend()
plt.show()