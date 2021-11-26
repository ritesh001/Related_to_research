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
import matplotlib.axes as ax
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
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel, WhiteKernel, \
RationalQuadratic, ExpSineSquared, DotProduct
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, \
precision_score, auc
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import shap
import lightgbm as lgb
import re

plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# plt.rc('text', usetex=True)

# =============================================================================
#        Different functions 
# =============================================================================
def extract_comp(arr):
    ind = arr.index
    comp = []
    for i in range(len(ind)):
        comp.append(data['Compound'].iloc[ind[i]])
    comp = pd.Series(comp)
    return comp
###----------------------------------------------------------------------------
    
data = pd.read_csv('final_elem+hard-feat_data.csv')
# data = data.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))

X = data.iloc[:,1:-1]
Y = data.iloc[:,-1]


# =============================================================================
#                    Model starts here
# =============================================================================
model = []
R2test = []
R2train = []
rmsetest = []
rmsetrain = []
print("Starting ML now...")

##------------------ DIVIDING INTO TEST AND TRAIN -------------------------------
start=7                 # start form zero 0 to get correct values of index in array
end=7
t_s=0.1
for random in range(start,end+1,1):
    print(random)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, 
                                                      test_size=t_s,random_state=random)
    # std_scale = preprocessing.StandardScaler().fit(X_train)
    # X_train_std = std_scale.transform(X_train)
    # X_test_std  = std_scale.transform(X_test)

### =============================================================================
###           STARTING ML MODEL
### =============================================================================

    params = {'objective': 'regression', 'boosting_type': 'gbdt', 'lambda_l1': 6.361891201722241e-06, 
              'lambda_l2': 0.058922915363507904, 'num_leaves': 41, 'feature_fraction': 0.5275591175500290, 
              'bagging_fraction': 0.9668053101704331, 'bagging_freq': 1, 'min_child_samples': 13, 
              'learning_rate': 0.09969741854704843}
    d_train = lgb.Dataset(X_train, label=Y_train)
    reg = lgb.train(params, d_train)                                               # changed X_train to X_train_std on 26-02-19
    # model.append(clf.kernel_)
    
    Y_pred_test = reg.predict(X_test)                                      # changed X_train to X_train_std on 26-02-19
    Y_pred_train = reg.predict(X_train)                                    # changed X_test to X_test_std on 26-02-19

#####---------------------- VALUES OF DIFFERENT PARAMS ---------------------------------
#
    R2_test = r2_score(Y_test,Y_pred_test)
    R2_train = r2_score(Y_train,Y_pred_train)
    print("R2 value train:  ", R2_train)
    print("R2 value test:  ", R2_test)
       
    rmse_test=np.sqrt(mean_squared_error(Y_test,Y_pred_test))
    rmse_train=np.sqrt(mean_squared_error(Y_train,Y_pred_train))
    print("RMSE train:  ", rmse_train)
    print("RMSE test:  ",  rmse_test)
    
    R2test.append(R2_test)
    R2train.append(R2_train)
    rmsetest.append(rmse_test)
    rmsetrain.append(rmse_train)


###### =============================================================================
######         Plotting (Do it only for best model)
###### =============================================================================
    # plt.subplots(figsize=(10,10))
    # plt.scatter(Y_train, Y_pred_train, 
                    # color = "orange", s = 30, label = 'Train data', edgecolors='black')
    # plt.scatter( Y_test, Y_pred_test,
                    # color = "cyan", s = 30, label = 'Test data', edgecolors='black') 
    xl = np.arange(-4,3,1)
    yl = np.arange(-4,3,1)
    plt.plot(yl, xl, linestyle='dashed', linewidth=1.0, color='black')  
    ##         plotting legend 
    # plt.legend(loc = 'upper left') 
    plt.tick_params(axis='both', direction='in')
    plt.xlabel('DFT (SCAN) $\Delta E_f$',fontsize=12)
    plt.ylabel('ML predicted $\Delta E_f$',fontsize=12)
    sns.scatterplot(x=Y_train, y=Y_pred_train, color="cyan", legend=False)
    sns.scatterplot(x=Y_test, y=Y_pred_test, color="orange", legend=False)
    plt.grid()
    # plt.savefig('result-ml_elem+hard.eps',dpi=360)
    #plt.show()

# ##------------------ SHAP PLOTS (uncomment only after finding best model) -------------------------------              
    # explainerModel = shap.TreeExplainer(model=reg)                             # change model accordingly
    # shap_values = explainerModel.shap_values(X_train)
    # shap.summary_plot(shap_values, X_train) ## Variable importance plot
    # shap.dependence_plot("geom-mean_eta_both", shap_values, X_train) ## SHAP dependence plot for the feature
#     shap.force_plot(explainerModel.expected_value, shap_values[0], X_train.iloc[[0]])   ## Individual SHAP value (change index of shap_values accordingly)
   
#####----------------------------------------------------------------------------------  

minrmsetest = min(rmsetest)  
ind=rmsetest.index(minrmsetest)  
avg_rmse_train = np.mean(rmsetrain)
avg_rmse_test = np.mean(rmsetest)
avg_r2_train = np.mean(R2train)
avg_r2_test = np.mean(R2test)
print("Random state is = ", start+ind)
print("Best R2 train/test =  ", R2train[ind]," / ", R2test[ind])
print("Best RMSE train/test = ", rmsetrain[ind]," / ",rmsetest[ind])
print("Avg R2 train/test =  ", avg_r2_train," / ", avg_r2_test)
print("Avg RMSE train/test = ", avg_rmse_train," / ",avg_rmse_test)

# =============================================================================
#              Printing predicted target value for all x
# =============================================================================
y_pred = reg.predict(X)
comp = data['Compound']
df = pd.concat([comp, X, Y, pd.Series(y_pred)], axis=1)
df.to_csv('final_pred-values_elem+hard.csv', index=False)