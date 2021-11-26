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
# import optuna.integration.lightgbm as lgb
import optuna

# =============================================================================
#        Different functions 
# =============================================================================
data = pd.read_csv('final_elem+hard-feat_data.csv')

X = data.iloc[:,1:-1]
Y = data.iloc[:,-1]

## Function for plotting ROC curve 
def plot_roc_cur(fper, tper):  
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()
    
def objective(trial):
    data, target = X, Y
    train_x, valid_x, train_y, valid_y = train_test_split(data, target, test_size=0.1)
    dtrain = lgb.Dataset(train_x, label=train_y)

    param = {
        "objective": "regression",
        "metric": "root_mean_squared_error",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 50),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.1),
    }

    gbm = lgb.train(param, dtrain)
    preds = gbm.predict(valid_x)
    # pred_labels = preds
    accuracy = np.sqrt(mean_squared_error(valid_y, preds))
    return accuracy
###----------------------------------------------------------------------------

# =============================================================================
#                    Model starts here
# =============================================================================

f = open('best-paramters_lgb_optuna_TPE.txt', 'a')
if __name__ == "__main__":
    # study = optuna.create_study(direction="maximize")
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=100)

    print("Number of finished trials: {}".format(len(study.trials)))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))
    f.write("  Value: {}\n".format(trial.value))

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value)) 
        f.write("    {}: {}\n".format(key, value))

f.write("\n")
f.close()
