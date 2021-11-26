#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:51:45 2019

@author: ritesh
"""
import warnings
warnings.filterwarnings('ignore')
#from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
# import matplotlib.axes as ax
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, LassoCV, \
    RidgeClassifier, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR, SVC
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel, WhiteKernel, \
RationalQuadratic, ExpSineSquared, DotProduct
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, \
precision_score, auc
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from  xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.inspection import permutation_importance
#plt.rc('font',family='Arial')
# plt.rc('text', usetex=True)
plt.rcParams['axes.labelsize'] = 30
plt.rcParams['axes.titlesize'] = 30
plt.rcParams['xtick.labelsize'] = 30
plt.rcParams['ytick.labelsize'] = 30
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

# =============================================================================
#        Different functions 
# =============================================================================

## Function for standardization
def stand(df):
    name = df.columns
    x=df.values
    ind=df.index
    std_scaler = preprocessing.StandardScaler()
    x_std=std_scaler.fit_transform(x)
    df_std = pd.DataFrame(x_std, columns=name,index=ind)
    df = df_std.copy()
    return (df)

## Function for finding correlation between features (from Rinkle)    
def corr_x_y(data, col):
    df = data
#    col = 'formation_energy'
    correlation_matrix = df.corr()
    correlation_type = correlation_matrix[col].copy()
    abs_correlation_type = correlation_type.apply(lambda x: abs(x))
    desc_corr_values = abs_correlation_type.sort_values(ascending=False)
    y_values = list(desc_corr_values.values)[1:]
    y_val1 = [ j for j in y_values if j>= 0.4 ]                                # show correlations with the value greater than j
    x_val1 = range(0,len(y_val1))
    x_val1 = range(0,len(y_val1))
    xlabels = list(desc_corr_values.keys())[1:len(x_val1)+1]
    fig, ax = plt.subplots(figsize=(10,10))
    ax.bar(x_val1, y_val1)
    ax.set_title('The correlation of all features with Formation Energies', fontsize=25)
    ax.set_ylabel('Pearson correlation coefficient', fontsize=16)
    plt.xticks(x_val1, xlabels, rotation='vertical')
    plt.tick_params(axis='both', which='major', labelsize=12)
    #plt.savefig('feature-kappa-correlation1.eps')
    #plt.show()
    #plt.savefig('/home/thsim6/Desktop/ML/vicker_hardness/binary_images/corr_features_90-10.png')

## Function for plotting ROC curve 
def plot_roc_cur(fper, tper):  
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()

###----------------------------------------------------------------------------
    
data = pd.read_csv('elem+hard_feat_all.csv')

X = data.iloc[:,1:-2]
Y = data.iloc[:,-1]
#imputer = Imputer(strategy="median")
imputer = SimpleImputer(strategy="median")
imputer.fit(X)
X_p = imputer.transform(X)
X_f = pd.DataFrame(X_p, columns=X.columns)
#X_std = stand(X_pp)                  # check this
#print("X:", X_std.head())
colnames = X_f.columns

df = pd.read_csv('ranking_elem+hard-feat.csv')
df_ = df[:15]

sel_feat = df_['Feature']
la = X_f.loc[:,sel_feat]
X_f1 = pd.DataFrame(la)

## ============================================================================
#                     Remove highly correlated features (only after checking correlation)
## ============================================================================
rem = ['avg ionic char', 'MagpieData avg_dev MeltingT', 'MagpieData mean SpaceGroupNumber', 'MagpieData maximum MeltingT'] # highly correlated features; to be removed
rem_no = [6, 12, 13, 14]
for col in rem:
    if col in X_f1.columns:
        del X_f1[col]
df_.drop(rem_no, inplace=True)
## ============================================================================
#                     Rectangular correlation plot
## ============================================================================
corr = X_f1.corr()
fig = plt.subplots(figsize=(50,50))
#sns.set(font_scale=5)
with sns.axes_style("white"):
    ax = sns.heatmap(corr, vmax=1, vmin=-1, fmt=".2f", linewidths=.5, square=True, \
                      annot=True, cmap='coolwarm', annot_kws={"size": 25, "weight": 'bold'})
sns.color_palette('bright')                                               # choose from colorblind, bright or muted
ax.set_xticklabels(df_['Features'])
ax.set_yticklabels(df_['Features'])
#plt.show()
#plt.xlabel('Features', fontsize=40)
#plt.ylabel('Features', fontsize=40)
plt.savefig('corr_ranked-feat.eps', dpi=300)
# -----------------------------------------------------------------------------

## ============================================================================
#                     Circular correlation plot
## ============================================================================
# sns.set_style(style="whitegrid")
# # Compute a correlation matrix and convert to long-form
# corr_mat = X_f1.corr().stack().reset_index(name="correlation")

# # Draw each cell as a scatter point with varying size and color
# g = sns.relplot(
#     data=corr_mat,
#     x="level_0", y="level_1", hue="correlation", size="correlation",
#     palette="bwr", hue_norm=(-1, 1), edgecolor=".7",
#     height=10, sizes=(50, 250), size_norm=(-0.2, 0.8), vmax=1, vmin=-1,
# )
# g.set(xlabel="", ylabel="", aspect="equal")
# g.despine(left=True, bottom=True)
# g.ax.margins(.02)
# for label in g.ax.get_xticklabels():
#     label.set_rotation(90)
# # for artist in g.legend.legendHandles:
#     # artist.set_edgecolor(".7")
# g.ax.set_xticklabels(df_['Features'])
# g.ax.set_yticklabels(df_['Features'])
# plt.show()
#------------------------------------------------------------------------------

# =============================================================================
#                  Feature ranking plot 
# =============================================================================
       
h = sns.catplot(x="Mean", y="Features", data = df_, kind="bar", 
                height=15, aspect=1.9, palette='Blues_r')
h.ax.set_xticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
sns.color_palette('bright')                                               # choose from colorblind, bright or muted
#plt.show()
#plt.xlabel('Mean Score', fontsize=40)
#plt.ylabel('Features', fontsize=40)
plt.savefig('feat-score_ranked.eps', dpi=300)

#f = open('imp-features_feat-rank.txt', 'w')
#f.write("%r\n" %(X_f1.columns))
#f.close()

#df_final = pd.concat([data['Compound'], X_f1, Y], axis=1)
#df_final.to_csv('final_elem+hard-feat_data.csv', index=False)
