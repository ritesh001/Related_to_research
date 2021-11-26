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
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import itertools as ir
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, LassoCV
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR, SVC
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel, WhiteKernel, \
RationalQuadratic, ExpSineSquared, DotProduct
from scipy.stats import norm
from math import floor, ceil
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, \
precision_score, auc
import sys

#plt.rc('font',family='Arial')

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
    
data = pd.read_csv('elem_feat_all_thermo-class.csv')
#rem_rows = [331, 1004, 87, 1025, 336, 1189, 1179, 1015, 477, 864, 575, 54, 537, 330, 490, 587, 340, 179, 602, 667, 1523, 22, 1233, 343, 1, 435, 58, 467, 1097, 912, 503, 388, 532, 534, 1496, 454, 1061, 936, 1183]
#data.drop(rem_rows, inplace=True)

X = data.iloc[:,1:-2]
Y = data.iloc[:,-1]
#imputer = Imputer(strategy="median")
imputer = SimpleImputer(strategy="median")
imputer.fit(X)
X_p = imputer.transform(X)
X_f = pd.DataFrame(X_p, columns=X.columns)
#X_std = stand(X_pp)                  # check this
#print("X:", X_std.head())

""" From Random Forests (feature importance) and removing correlated features"""
sel_feat = ['MagpieData minimum CovalentRadius', 'MagpieData avg_dev GSbandgap',
       'minimum EN difference', 'MagpieData avg_dev MendeleevNumber',
       'MagpieData mean GSbandgap', 'maximum EN difference',
       'MagpieData avg_dev NpValence', 'avg anion electron affinity',
       'MagpieData mean SpaceGroupNumber', 'MagpieData maximum MeltingT']
la = X_f.loc[:,sel_feat]
X_f = pd.DataFrame(la)


### =============================================================================
###                          INITIALIZATION...
### =============================================================================
acctest = []; acctrain = []
f1test = []; f1train = []
prectrain = []; prectest = []
#model = []
print("Starting ML now...")

##------------------ DIVIDING INTO TEST AND TRAIN -------------------------------
start = int(sys.argv[1])                 # start form zero 0 to get correct values of index in array
end = int(sys.argv[2])
t_s = float(sys.argv[3])
for random in range(start,end+1,1):
    print(random)
    X_train, X_test, Y_train, Y_test = train_test_split(X_f,Y, 
                                                      test_size=t_s,random_state=random)
    std_scale = preprocessing.StandardScaler().fit(X_train)
    X_train_std = std_scale.transform(X_train)
    X_test_std  = std_scale.transform(X_test)

### =============================================================================
###           STARTING ML MODEL
### =============================================================================
    
    clf = SVC(kernel='rbf', gamma='auto')
    clf.fit(X_train_std,Y_train)                                               # changed X_train to X_train_std on 26-02-19
    #model.append(clf.kernel_)
    
    Y_pred_test = clf.predict(X_test_std)                                      # changed X_train to X_train_std on 26-02-19
    Y_pred_train = clf.predict(X_train_std)                                    # changed X_test to X_test_std on 26-02-19

#####---------------------- VALUES OF DIFFERENT PARAMS ---------------------------------
    #acc_test = accuracy_score(Y_test,Y_pred_test, normalize=False)
    acc_test = accuracy_score(Y_test,Y_pred_test)
    acc_train = accuracy_score(Y_train,Y_pred_train)
    print("Accuracy train:  ", acc_train)           # test_data, vicker_test 
    print("Accuracy test:  ", acc_test)
       
    #f1_test=f1_score(Y_test,Y_pred_test,average='micro')
    f1_test = f1_score(Y_test,Y_pred_test,average='weighted')
    f1_train = f1_score(Y_train,Y_pred_train,average='weighted')
    print("F1 train:  ", f1_train)
    print("F1 test:  ",  f1_test)
    
    prec_test = precision_score(Y_test,Y_pred_test,average='weighted')
    prec_train = precision_score(Y_train,Y_pred_train,average='weighted')
    print("Precision train:  ", prec_train)           # test_data, vicker_test 
    print("Precision test:  ", prec_test)
    
    acctest.append(acc_test)
    acctrain.append(acc_train)
    f1test.append(f1_test)
    f1train.append(f1_train)
    prectrain.append(prec_train)
    prectest.append(prec_test)
###----------------------------------------------------------------------------------
   
### =============================================================================
###           FINAL RESULTS
### =============================================================================    
minacctest = max(acctest)  
ind=acctest.index(minacctest)  
print("Random state is = ", start+ind)
print("Accuracy train/test =  ",acctrain[ind]," / ", acctest[ind])
print("F1 train/test = ",f1train[ind]," / ",f1test[ind])
print("Precision train/test =  ",prectrain[ind]," / ", prectest[ind])
avgacc_train = np.mean(acctrain)
avgacc_test = np.mean(acctest)
avgf1_train = np.mean(f1train)
avgf1_test = np.mean(f1test)
avgprec_train = np.mean(prectrain)
avgprec_test = np.mean(prectest)

### =============================================================================
###           FROM BEST ML MODEL
### =============================================================================    
X_tr, X_te, Y_tr, Y_te = train_test_split(X_f, Y, test_size = t_s, random_state = ind)
std_scale = preprocessing.StandardScaler().fit(X_tr)
X_tr_std = std_scale.transform(X_tr)
X_te_std  = std_scale.transform(X_te)
clf.fit(X_tr_std, Y_tr)
Y_pred = clf.predict(X_te_std)
cm = confusion_matrix(Y_te, Y_pred)
cts_ = Y_te.value_counts()
cls = cts_.index
cts = cts_.ravel()
print(cls, cts)
print("Confusion matrix for test:")
print(cm)
Y_pred_tot = clf.predict(X_f)
cm_tot = confusion_matrix(Y, Y_pred_tot)
print("Confusion matrix for all:")
print(cm_tot)
### only for binary class
#probs = clf.predict_proba(X_te_std)  
#probs = probs[:, 1]
#roc = roc_auc_score(Y_test, probs, average='weighted')
#fper, tper, thresholds = roc_curve(Y_test, probs) 
#plot_roc_curve(fper, tper)


### =============================================================================
###          OUTPUT TO A FILE 
### =============================================================================    
f = open('save-result.txt', 'a')
f.write("Method used = %r\n" %(clf))
f.write("No of data points = %d\n" %(len(data)))
f.write("features used = %s\n" %(X_f.columns))
f.write("No of features = %d\n" %(len(X_f.columns)))
#f.write("best model = %s\n" %(model[ind]))
f.write("test size in ratio = %f\n" %(t_s))
f.write("Random state is = %d\n" %(start+ind))
f.write("Best Accuracy train/test =  %f / %f\n" %(acctrain[ind], acctest[ind]))
f.write("Best F1 train/test = %f / %f\n" %(f1train[ind], f1test[ind]))
f.write("Best Precision train/test =  %f / %f\n" %(prectrain[ind], prectest[ind]))
#f.write("Best ROC train/test = %f / %f\n" %(roctrain[ind], roctest[ind]))
f.write("Avg Accuracy train/test =  %f / %f\n" %(avgacc_train, avgacc_test))
f.write("Avg F1 train/test =  %f / %f\n" %(avgf1_train, avgf1_test))
f.write("Avg Precision train/test =  %f / %f\n" %(avgprec_train, avgprec_test))
f.write("Counts of Y(test) = %s: %d, %s: %d, %s, %d\n" %(cls[0], cts[0], cls[1], cts[1],\
cls[2], cts[2]))
f.write("Confusion matrix for test:\n")
f.write("%r\n" %(cm))
f.write("Confusion matrix for all:\n")
f.write("%r\n" %(cm_tot))
f.write("\n")
f.close()
