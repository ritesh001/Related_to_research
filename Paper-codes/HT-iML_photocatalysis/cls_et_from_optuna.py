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
import pandas as pd
import numpy as np
# import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, LassoCV, \
    RidgeClassifier, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR, SVC
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, \
ExtraTreesClassifier
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel, WhiteKernel, \
RationalQuadratic, ExpSineSquared, DotProduct
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, \
precision_score, auc, matthews_corrcoef
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from imblearn.over_sampling import SMOTE

plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# plt.rc('text', usetex=True)

# =============================================================================
#        Different functions 
# =============================================================================

def read_param():
    f0 = open('best-paramters_et_optuna_TPE.txt','r')
    b = []
    for line in f0.readlines():
        a = line.split()
        a_ = [a[i] for i in range(len(a))]
        b.append(a_)
    f0.close()
    p1 = int(b[1][1]); p2 = int(b[2][1]); p3 = int(b[3][1]); p4 = int(b[4][1])
    p5 = float(b[5][1]); p6 = int(b[6][1])
    return p1, p2, p3, p4, p5, p6
###----------------------------------------------------------------------------
    
data = pd.read_csv('final_elem+hard-feat_data_cls_com.csv')

X = data.iloc[:,1:-1]
Y = data.iloc[:,-1]

# =============================================================================
#                    Model starts here
# =============================================================================
print("Starting ML now...")
p1, p2, p3, p4, p5, p6 = read_param()
##------------------ DIVIDING INTO TEST AND TRAIN -------------------------------
start = 0                 # start form zero 0 to get correct values of index in array
end_1 = 10
end_2 = 200
t_s = 0.1
for random_sm in range(start, end_1+1, 1):
#for random_sm in range(6, end_1+1, 1):
    print("SMOTE counter =", random_sm)
    acctest = []; acctrain = []
    f1test = []; f1train = []
    prectrain = []; prectest = []
    mcctest = []; mcctrain = []
    #model = []
    for random in range(start, end_2+1, 1):
        print(random_sm, random)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=t_s,
                                                            random_state=random, stratify=Y)
        #dict = {2:100, 3:150, 6:100}
        dict = {2:100, 6:100}
        oversample = SMOTE(sampling_strategy=dict, random_state=random_sm)
        #oversample = SMOTE(sampling_strategy='not majority', random_state=random_sm)
        x_train_sm, y_train_sm = oversample.fit_resample(X_train, Y_train)
    
    ### =============================================================================
    ###           STARTING ML MODEL
    ### =============================================================================
        
        #weights = {0:3.0, 1:1.0, 2:3.0, 3:3.0, 4:0.5, 5:1.0, 6:3.0, 7:1.3, 8:1.6}
        weights = {0:3.0, 1:1.0, 2:3.0, 3:3.0, 4:0.8, 5:1.0, 6:3.0, 7:1.6, 8:1.9} # --> best one till now
        #weights = {0:3.0, 1:1.0, 2:3.0, 3:3.0, 4:1.0, 5:1.2, 6:3.0, 7:1.6, 8:1.9} 
        #weights = {0:3.0, 1:1.0, 2:3.0, 3:3.0, 4:1.0, 5:1.0, 6:3.0, 7:1.6, 8:1.9} 
        #weights = "balanced"
        params = {"class_weight": weights, "n_estimators": p1, "max_depth": p2, "criterion": "entropy",
                  'min_samples_leaf': p3, 'min_samples_split': p4, 'min_weight_fraction_leaf': p5, "random_state": p6 
                  }
        et = ExtraTreesClassifier(**params)
        #et = ExtraTreesClassifier(**params, random_state=0)
        et.fit(x_train_sm, y_train_sm)
        # model.append(clf.kernel_)
        
        Y_pred_test = et.predict(X_test)
        Y_pred_train = et.predict(x_train_sm)
        # Y_pred_test_ = [np.argmax(line) for line in Y_pred_test]
        # Y_pred_train_ = [np.argmax(line) for line in Y_pred_train]
    
    #####---------------------- VALUES OF DIFFERENT PARAMS ---------------------------------

        acc_test = accuracy_score(Y_test,Y_pred_test)
        acc_train = accuracy_score(y_train_sm,Y_pred_train)
        print("Accuracy train:  ", acc_train)            
        print("Accuracy test:  ", acc_test)
           
        #f1_test=f1_score(Y_test,Y_pred_test,average='micro')
        f1_test = f1_score(Y_test,Y_pred_test,average='macro')
        f1_train = f1_score(y_train_sm,Y_pred_train,average='macro')
        print("F1 train:  ", f1_train)
        print("F1 test:  ",  f1_test)
        
        prec_test = precision_score(Y_test,Y_pred_test,average='macro')
        prec_train = precision_score(y_train_sm,Y_pred_train,average='macro')
        print("Precision train:  ", prec_train)          
        print("Precision test:  ", prec_test)
        
        mcc_test = matthews_corrcoef(Y_test,Y_pred_test)
        mcc_train = matthews_corrcoef(y_train_sm,Y_pred_train)
        print("MCC train:  ", mcc_train)            
        print("MCC test:  ", mcc_test)
        
        acctest.append(acc_test)
        acctrain.append(acc_train)
        f1test.append(f1_test)
        f1train.append(f1_train)
        prectrain.append(prec_train)
        prectest.append(prec_test)
        mcctest.append(mcc_test)
        mcctrain.append(mcc_train)
    
    
    maxacctest = max(mcctest)  
    ind = mcctest.index(maxacctest)  
    print("Best random state for model counter is = ", start+ind)
    print("Random state for SMOTE counter is = ", random_sm)
    print("Accuracy train/test =  ", acctrain[ind]," / ", acctest[ind])
    print("F1 train/test = ", f1train[ind]," / ",f1test[ind])
    print("Precision train/test =  ", prectrain[ind]," / ", prectest[ind])
    print("MCC train/test =  ", mcctrain[ind]," / ", mcctest[ind])
    avgacc_train = np.mean(acctrain)
    avgacc_test = np.mean(acctest)
    avgf1_train = np.mean(f1train)
    avgf1_test = np.mean(f1test)
    avgprec_train = np.mean(prectrain)
    avgprec_test = np.mean(prectest)
    avgmcc_train = np.mean(mcctrain)
    avgmcc_test = np.mean(mcctest)
    
    ###### =============================================================================
    ######         Writing to a file
    ###### =============================================================================
    f = open('save-result_et_10.txt', 'a')
    f.write("No of data points = %d\n" %(len(data)))
    f.write("test size in ratio = %f\n" %(t_s))
    f.write("features used = %s\n" %(X.columns))
    f.write("No of features = %d\n" %(len(X.columns)))
    # f.write("Best model = %s\n" %(model[ind]))
    f.write("Best random state for model counter = %d\n" %(ind))
    f.write("Random state for SMOTE counter = %d\n" %(random_sm))
    f.write("Model used = %s\n" %(et.get_params()))
    f.write("Best Accuracy train/test =  %f / %f\n" %(acctrain[ind], acctest[ind]))
    f.write("Best F1 train/test = %f / %f\n" %(f1train[ind], f1test[ind]))
    f.write("Best Precision train/test =  %f / %f\n" %(prectrain[ind], prectest[ind]))
    f.write("Best MCC train/test =  %f / %f\n" %(mcctrain[ind], mcctest[ind]))
    f.write("Avg Accuracy train/test =  %f / %f\n" %(avgacc_train, avgacc_test))
    f.write("Avg F1 train/test =  %f / %f\n" %(avgf1_train, avgf1_test))
    f.write("Avg Precision train/test =  %f / %f\n" %(avgprec_train, avgprec_test))
    f.write("Avg MCC train/test =  %f / %f\n" %(avgmcc_train, avgmcc_test))
    f.write("\n")
    f.close()
