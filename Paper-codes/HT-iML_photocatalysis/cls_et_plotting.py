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
#import seaborn as sns
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
precision_score, auc, plot_confusion_matrix, matthews_corrcoef, classification_report
import sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
# import shap
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from imblearn.combine import SMOTETomek
from collections import Counter
from imblearn.pipeline import make_pipeline

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

target_names = ['Hh', 'Hm', 'Hl', 'Mh', 'Mm', 'Ml', 'Lh', 'Lm', 'Ll']
ticks = [i for i in range(9)]
def count_class(X):
    counter = Counter(X)
    # plot the distribution
    plt.bar(counter.keys(), counter.values())
    plt.xticks(ticks=ticks, labels=target_names)
    plt.show()    
    for k,v in counter.items():
        per = v / len(Y) * 100
#         print('Class=%d, n=%d (%.3f%%)' % (k, v, per))
        print('Class=%s, n=%d (%.3f%%)' % (target_names[k], v, per))
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
t_s = 0.1
#random = 123
#random_sm = 7
random = 129
random_sm = 0
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=t_s,
                                                    random_state=random, stratify=Y)
#dict = {2:100, 3:150, 6:100}
dict = {2:100, 6:100}
oversample = SMOTE(sampling_strategy=dict, random_state=random_sm)
x_train_sm, y_train_sm = oversample.fit_resample(X_train, Y_train)
#count_class(y_train_sm)
#count_class(Y_test)
# std_scale = preprocessing.StandardScaler().fit(X_train)
# X_train_std = std_scale.transform(X_train)
# X_test_std  = std_scale.transform(X_test)

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
f1_test = f1_score(Y_test,Y_pred_test,average='weighted')
f1_train = f1_score(y_train_sm,Y_pred_train,average='weighted')
print("F1 train:  ", f1_train)
print("F1 test:  ",  f1_test)

prec_test = precision_score(Y_test,Y_pred_test,average='weighted')
prec_train = precision_score(y_train_sm,Y_pred_train,average='weighted')
print("Precision train:  ", prec_train)           # test_data, vicker_test 
print("Precision test:  ", prec_test)

mcc_test = matthews_corrcoef(Y_test,Y_pred_test)
mcc_train = matthews_corrcoef(y_train_sm,Y_pred_train)
print("MCC train:  ", mcc_train)    
print("MCC test:  ", mcc_test)
# =============================================================================
#          ROC-AUC Curves
# =============================================================================
pred = Y_pred_test
pred_prob = et.predict_proba(X_test)

fpr = {}
tpr = {}
auc_score = {}
thresh = {}

n_class = 9

colors = ['orange', 'green', 'blue', 'cyan', 'purple', 'teal', 'red', 'lime', 'grey']
for i in range(n_class):    
    fpr[i], tpr[i], thresh[i] = roc_curve(Y_test, pred_prob[:,i], pos_label=i)
#     auc_score[i] = roc_auc_score(y_test, pred_prob[:,i], multi_class='ovr', average='weighted')
    auc_score[i] = auc(fpr[i], tpr[i])   ## auc is more general than roc_auc_score and more meaningful in imbalanced cases
    print(auc_score[i])
    label = target_names[i] + ', AUC = ' + str(auc_score[i])
    plt.plot(fpr[i], tpr[i], linestyle='--', color=colors[i], label=label)

plt.title('Multiclass ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive rate')
plt.legend(loc='best')
#plt.show()
#plt.savefig('roc_et_mcc.eps', dpi=300)
###----------------------------------------------------------------------------

# =============================================================================
#         Confusion Matrix
# =============================================================================
title = 'Confusion matrix for XGB classifier'
# cm = confusion_matrix(y_test, y_pred_test)
Y_pred = et.predict(X)
cm = confusion_matrix(Y, Y_pred)
print(cm)
disp = plot_confusion_matrix(et,
                             X,
                             Y,
                             display_labels=target_names,
                             cmap=plt.cm.Blues,
                             normalize=None,
                            )
disp.ax_.set_title(title)
#plt.show()
#plt.savefig('cm_et_mcc.eps', dpi=300)
###----------------------------------------------------------------------------

# =============================================================================
#         Confusion Matrix
# =============================================================================
report = classification_report(Y, Y_pred)
print("Classification report:-")
print(report)
