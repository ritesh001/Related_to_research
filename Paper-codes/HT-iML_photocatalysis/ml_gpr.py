#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:51:45 2019

@author: ritesh
"""
import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import Imputer
#from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn import svm
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import itertools as ir
from sklearn.kernel_ridge import KernelRidge
import seaborn as sns
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from scipy import stats
#from bayes_opt import BayesianOptimization
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, RBF
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib
from sklearn.metrics import mean_absolute_error
import scipy
from sklearn.kernel_ridge import KernelRidge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split 
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.model_selection import RandomizedSearchCV
from sklearn.gaussian_process.kernels import Matern, ConstantKernel, RationalQuadratic, ExpSineSquared, DotProduct
import seaborn as sns
from sklearn.metrics import r2_score
from scipy import stats
from scipy.stats import norm
from math import floor, ceil
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.linear_model import LogisticRegression

#plt.rc('font',family='Arial')

# =============================================================================
#        Different functions 
# =============================================================================

## Function for residual plot
def resdi(y_te,y_tr,y_test,y_train):
#    fig, ax = plt.subplots(figsize=(8,8))
    p=[]
    for i in range(len(y_te)):
        pp=y_te[i]-y_test.values[i]
        p.append(pp)
#        ax.plot([y_test.index.values[i],y_test.index.values[i]],[y_test.values[i]-y_test.values[i], p[i]], c="orange", linewidth=2)
#    ax.plot(y_test.index.values,y_test.values-y_test.values,'o', markersize=3,label='measured-test', color = 'black')
#    ax.plot(y_test.index.values,p,'o',markersize=3, label='predicted-test', color = 'red' )
    q=[]
    for i in range(len(y_tr)):
        qq=y_tr[i]-y_train.values[i]
        q.append(qq)
#        ax.plot([y_train.index.values[i],y_train.index.values[i]],[y_train.values[i]-y_train.values[i], q[i]], c="b", linewidth=2)
#    ax.plot(y_train.index.values,y_train.values-y_train.values,'o', markersize=3,label='measured-train', color = 'grey')
#    ax.plot(y_train.index.values,q,'o',markersize=3, label='predicted-train', color = 'dodgerblue')
#    ax.legend()	
    ch = []
    for i in range(len(p)):
        if abs(p[i]) >= 0.3:                                                        # condition for calling out
           ch.append(y_test.index.values[i])

    for j in range(len(q)):
        if abs(q[j]) >= 0.3:
           ch.append(y_train.index.values[j])
    return ch 

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

## Function for finding correlation between features (from Avanish)
def corr_x(X):
    idx = np.abs(np.tril(X, k= -1)) < 0.1
    idx_drop = np.all(idx[0,:], axis=0)
    cold = X.columns[~idx_drop]
    junk = X.copy()
    junk = junk.drop(cold, axis = 1)
    junk.shape
    comp = junk.copy()
    corr = X.corr()
    #mask = np.zeros_like(corr)
    #mask[np.triu_indices_from(mask)] = True
    fig = plt.subplots(figsize=(30,30))
    with sns.axes_style("white"):
        ax = sns.heatmap(corr, vmax=1,vmin=-1,fmt=".2f", linewidths=.5,square=True,annot=True,cmap='bwr',annot_kws={"size": 10, "weight": 'bold'})
    comp = stand(comp)

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
    x_values = range(0,len(y_val1))
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

###----------------------------------------------------------------------------
    
data = pd.read_csv('data1_1.csv')
rem_rows = [331, 1004, 87, 1025, 336, 1189, 1179, 1015, 477, 864, 575, 54, 537, 330, 490, 587, 340, 179, 602, 667, 1523, 22, 1233, 343, 1, 435, 58, 467, 1097, 912, 503, 388, 532, 534, 1496, 454, 1061, 936, 1183]
data.drop(rem_rows, inplace=True)

X = data.iloc[:,1:-1]
Y = data.iloc[:,-1]
imputer = Imputer(strategy="median")
#imputer = SimpleImputer(strategy="median")
imputer.fit(X)
X_p = imputer.transform(X)
X_f = pd.DataFrame(X_p, columns=X.columns)
#X_std = stand(X_pp)                  # check this
#print("X:", X_std.head())

## ============================================================================
#                     Reducing features using LassoCV
## ============================================================================
#lcv = LassoCV()
#y_te=lcv.fit(X_f, Y.values.ravel())
#a=y_te.coef_.nonzero()
#X_f.columns[a]
#imp = X_f.columns[a]
#print("-------------After applying LassoCV-------------------------------------------")
#print(imp)
#print("------------------------------------------------------------------------------")
#la = X_f.ix[:,imp]
#X_f = pd.DataFrame(la)
##print(X_std.head())
##X_std.to_csv('tmp.csv'.sep=",")
#
#idx = np.abs(np.tril(X_f, k= -1)) < 0.1
#idx_drop = np.all(idx[0,:], axis=0)
#cold = X_f.columns[~idx_drop]
#junk = X_f.copy()
#junk = junk.drop(cold, axis = 1)
#junk.shape
#comp = junk.copy()
####----------------------------------------------------------------------------

## ============================================================================
#                     Remove highly correlated features
## ============================================================================
#threshold = 0.8
#corr = X_f.corr()
#col_corr = set()
#for i in range(len(corr.columns)):
#    for j in range(i):
#        if corr.iloc[i, j] >= threshold:
#            colname = corr.columns[i] # getting the name of column
#            col_corr.add(colname)
#            if colname in X_f.columns:
#                del X_f[colname]
#print("-------After removing highly correlated features------------------------------")
#print(X_f.columns)
#print("------------------------------------------------------------------------------")
##----------------------------------------------------------------------------
#corr_x(X_f)
#new_data = pd.DataFrame(X_f)
#corr_x_y(new_data, 'formation_energy')

""" Fatures from Random Forests """
#sel_feat = ['range MeltingT', 'avg_dev AtomicWeight', 'avg_dev CovalentRadius',
#       'range GSvolume_pa', 'max ionic char', 'range MendeleevNumber',
#       'mean AtomicWeight', 'minimum Electronegativity',
#       'minimum MendeleevNumber']
""" From LASSO (on all data) and removing correlated features"""
sel_feat = ['avg_dev MendeleevNumber', 'range AtomicWeight', 'mean AtomicWeight',
       'minimum MeltingT', 'maximum MeltingT', 'mean CovalentRadius',
       'avg_dev CovalentRadius', 'maximum NfValence', 'range NValence',
       'maximum NUnfilled', 'maximum SpaceGroupNumber',
       'range SpaceGroupNumber', 'mean SpaceGroupNumber',
       'mode SpaceGroupNumber']
la = X_f.ix[:,sel_feat]
X_f = pd.DataFrame(la)

# =============================================================================
#                    Model starts here
# =============================================================================
model = []
R2test = []
R2train = []
rmsetest = []
rmsetrain = []
#
##------------------ DIVIDING INTO TEST AND TRAIN -------------------------------
start=0                 # start form zero 0 to get correct values of index in array
end=200
t_s=0.1
for random in range(start,end+1,1):
    print(random)
    X_train, X_test, Y_train, Y_test = train_test_split(X_f,Y, 
                                                      test_size=t_s,random_state=random)
    std_scale = preprocessing.StandardScaler().fit(X_train)
    X_train_std = std_scale.transform(X_train)
    X_test_std  = std_scale.transform(X_test)

### =============================================================================
###           STARTING GPR MODEL
### =============================================================================
###
    kernel = 1.0 * Matern(length_scale=1.0, length_scale_bounds=(10**-1, 10**1), nu=0.5) +   WhiteKernel(noise_level=1e-1, noise_level_bounds=(1e-1, 1e+1))
    #kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) + \
    #WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-10, 1e+1))
    
    reg = GaussianProcessRegressor(kernel=kernel,  alpha=1e-10,
    optimizer = 'fmin_l_bfgs_b', n_restarts_optimizer=30, normalize_y=False,
    copy_X_train = True, random_state=1)    
    reg.fit(X_train_std,Y_train)                                               # changed X_train to X_train_std on 26-02-19
    model.append(reg.kernel_)
    
    Y_pred_test = reg.predict(X_test_std)                                      # changed X_train to X_train_std on 26-02-19
    Y_pred_train = reg.predict(X_train_std)                                    # changed X_test to X_test_std on 26-02-19

# =============================================================================
#           STARTING KRR MODEL
# =============================================================================
#    kernel = 1.0 * Matern(length_scale=1.0, length_scale_bounds=(10**-1, 10**1), nu=0.1)

#    reg=KernelRidge(alpha=0.00001, kernel=kernel,gamma=1,coef0=499)
#    kr.fit(X_train_std,Y_train)
#    Y_pred_test = kr.predict(X_test_std)
#    Y_pred_train = kr.predict(X_train_std)

#####---------------------- VALUES OF DIFFERENT PARAMS ---------------------------------
#
    R2_test=metrics.r2_score(Y_test,Y_pred_test)
    R2_train=metrics.r2_score(Y_train,Y_pred_train)
#    print("R2 value train:  ", R2_train)           # test_data, vicker_test 
#    print("R2 value test:  ", R2_test)
       
    rmse_test=np.sqrt(metrics.mean_squared_error(Y_test,Y_pred_test))
    rmse_train=np.sqrt(metrics.mean_squared_error(Y_train,Y_pred_train))
#    print("mean square error train:  ", rmse_train)
#    print("mean square error test:  ",  rmse_test)
    
    R2test.append(R2_test)
    R2train.append(R2_train)
    rmsetest.append(rmse_test)
    rmsetrain.append(rmse_train)

#
###----------------------------------------------------------------------------------
#
#
#####---------------------------------   PLOTTING GRAPH -------------------------------------------------------------
#    plt.subplots(figsize=(5,5))
#    plt.scatter(Y_train, Y_pred_train, 
#                    color = "green", s = 10, label = 'Train data') 
#          
#    # #        plotting residual errors in test data 
#    plt.scatter( Y_test, Y_pred_test,
#                    color = "blue", s = 10, label = 'Test data') 
#            
#    ##         plotting line for zero residual error 
#    #    plt.hlines(y=0, xmin = 0, xmax = 7, linewidth = 2) 
#    xl=[0,1,2,3,4,5,6,7]
#    yl=[0,1,2,3,4,5,6,7]
#    plt.plot(yl,xl,linestyle='dashed', linewidth=0.5)  
#    ##         plotting legend 
#    plt.legend(loc = 'upper left') 
#      
#    ##         plot title 
##    plt.title("Residual errors") 
#    
#    ##         plot label
##    plt.tick_params(axis='both', which='major', labelsize=15)
#    plt.xlabel('actual Hv',fontsize=15)
#    plt.ylabel("predicted Hv",fontsize=15)
##    plt.savefig('GPR.png',dpi=360)
#    plt.show()
#
   
#####----------------------------------------------------------------------------------  
#
#
minrmsetest = min(rmsetest)  
ind=rmsetest.index(minrmsetest)  
print("Random state is = ", start+ind)
print("R2 train/test =  ",R2train[ind]," / ", R2test[ind])
print("RMSE train/test = ",rmsetrain[ind]," / ",rmsetest[ind])
#   
###### =============================================================================
######         Plotting residuals
###### =============================================================================
#
#
out_ind = resdi(Y_pred_test,Y_pred_train,Y_test,Y_train)

f = open('save-result.txt', 'a')
f.write("No of data points = %d\n" %(len(data)))
f.write("features used = %s\n" %(X_f.columns))
f.write("No of features = %d\n" %(len(X_f.columns)))
f.write("best model = %s\n" %(model[ind]))
f.write("test size in ratio = %f\n" %(t_s))
f.write("Random state is = %d\n" %(start+ind))
f.write("R2 train/test =  %f / %f\n" %(R2train[ind], R2test[ind]))
f.write("RMSE train/test = %f / %f\n" %(rmsetrain[ind], rmsetest[ind]))
f.write("Index of outliers = %s\n" %(out_ind))
#f.write("RMSE on unseen data = %f\n" %(rmse_un))
f.write("\n")
f.close()
