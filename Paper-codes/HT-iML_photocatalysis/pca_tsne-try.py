# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 19:33:44 2020

@author: ritesh
"""

from __future__ import print_function
import time
import numpy as np
import pandas as pd
#from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn import preprocessing

data_ = pd.read_csv('tt.csv')
data = pd.read_csv('jarvis_feat_30-06-20.csv')
X = data.iloc[:,1:-2]                                                         # change accordingly
#y = data_.iloc[:,-3]
feat_cols = X.columns

##
def is_stable(n):
	form = data['Formation_energy'][n]
	if form <= 0:
		return 'stable'
	else:
		return 'unstable'

y = []
ox = data_['M_oxid_state']
for i in range(len(data_)):
	y.append(str(ox[i]) + '-' + is_stable(i))

std_scale = preprocessing.StandardScaler().fit(X)
X = std_scale.transform(X)

df = pd.DataFrame(X,columns=feat_cols)
df['y'] = y
df['label'] = df['y'].apply(lambda i: str(i))

X, y = None, None

np.random.seed(42)
rndperm = np.random.permutation(df.shape[0])

##-----------PCA------------##
#pca = PCA(n_components=3)
#pca_result = pca.fit_transform(df[feat_cols].values)
#df['pca-one'] = pca_result[:,0]
#df['pca-two'] = pca_result[:,1] 
#df['pca-three'] = pca_result[:,2]
#print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
#
#plt.figure(figsize=(16,10))
#sns.scatterplot(
#    x="pca-one", y="pca-two",
#    hue="y",
#    palette=sns.color_palette("hls", 6),
#    data=df.loc[rndperm,:],
#    legend="full",
#    alpha=0.3
#)

##----------tSNE-----------##
time_start = time.time()
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(df[feat_cols].values)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

df['tsne-2d-one'] = tsne_results[:,0]
df['tsne-2d-two'] = tsne_results[:,1]
df['Formation_energy'] = data['Formation_energy']
plt.figure(figsize=(16,10))
sns.set_context("paper", rc={"font.size":15,"axes.titlesize":15,"axes.labelsize":15})
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    hue="y",
    palette=sns.color_palette("Set2", 6),
#	size="Formation_energy",
    data=df,
    legend="full",
    alpha=0.5,
	s=100
)