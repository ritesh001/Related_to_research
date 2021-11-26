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

plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# plt.rc('text', usetex=True)

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
        # ax = sns.heatmap(corr, vmax=1,vmin=-1,fmt=".2f", linewidths=.5,square=True,annot=True,cmap='bwr',annot_kws={"size": 10, "weight": 'bold'})
        ax = sns.heatmap(corr,linewidths=0.25,vmax=1.0, square=True, cmap="cubehelix", linecolor='k', annot=True)
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
    
data = pd.read_csv('final_elem+hard-feat_data.csv')


X = data.iloc[:,1:-1]
Y = data.iloc[:,-1]

## For printing final csv file containing only selected features
# frames = [X_f, Y]
# new = pd.concat(frames, axis=1)
# new.to_csv('final-feat_data.csv')

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
start=0                 # start form zero 0 to get correct values of index in array
end=200
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
              'lambda_l2': 0.05892291536350790400, 'num_leaves': 41, 'feature_fraction': 0.5275591175500290, 
              'bagging_fraction': 0.9668053101704331, 'bagging_freq': 1, 'min_child_samples': 13,
              'learning_rate': 0.09969741854704843}                          ## from TPE sampler method
    
    # params = {'objective': 'regression', 'boosting_type': 'gbdt', 'lambda_l1': 2.205066989044768e-07, 
    #           'lambda_l2': 0.00011370018782361723, 'num_leaves': 31, 'feature_fraction': 0.4, 
    #           'bagging_fraction': 1.0, 'bagging_freq': 0, 'min_child_samples': 20, 
    #           'num_iterations': 1000, 'learning_rate': 0.073}                ## from inbuilt optimizer in Optuna for LGBM
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
#     plt.subplots(figsize=(5,5))
#     plt.scatter(Y_train, Y_pred_train, 
#                     color = "orange", s = 25, label = 'Train data', edgecolors='black') 
          
#     # #        plotting residual errors in test data 
#     plt.scatter( Y_test, Y_pred_test,
#                     color = "cyan", s = 25, label = 'Test data', edgecolors='black') 
            
#     ##         plotting line for zero residual error 
#     #    plt.hlines(y=0, xmin = 0, xmax = 7, linewidth = 2) 
#     xl = np.arange(-4,3,1)
#     yl = np.arange(-4,3,1)
#     plt.plot(yl, xl, linestyle='dashed', linewidth=2.0, color='red')  
#     ##         plotting legend 
#     plt.legend(loc = 'upper left') 
      
#     ##         plot title 
# #    plt.title("Residual errors") 
    
#     ##         plot label
# #    plt.tick_params(axis='both', which='major', labelsize=15)
#     plt.xlabel('DFT (SCAN) $\Delta E_f$',fontsize=12)
#     plt.ylabel('ML predicted $\Delta E_f$',fontsize=12)
# #    plt.savefig('GPR.png',dpi=360)
#     plt.show()

# ##------------------ SHAP PLOTS (uncomment only finding best model) -------------------------------              
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
   
###### =============================================================================
######         Plotting residuals
###### =============================================================================
# out_ind = resdi(Y_pred_test,Y_pred_train,Y_test,Y_train)

###### =============================================================================
######         Writing to a file
###### =============================================================================
f = open('save-result.txt', 'a')
f.write("No of data points = %d\n" %(len(data)))
f.write("features used = %s\n" %(X.columns))
f.write("No of features = %d\n" %(len(X.columns)))
# f.write("Best model = %s\n" %(model[ind]))
f.write("Best random state = %d\n" %(ind))
f.write("Model used = %s\n" %(reg.params))
f.write("test size in ratio = %f\n" %(t_s))
f.write("Random state is = %d\n" %(start+ind))
f.write("Best R2 train/test =  %f / %f\n" %(R2train[ind], R2test[ind]))
f.write("Best RMSE train/test = %f / %f\n" %(rmsetrain[ind], rmsetest[ind]))
f.write("Avg R2 train/test =  %f / %f\n" %(avg_r2_train, avg_r2_test))
f.write("Avg RMSE train/test = %f / %f\n" %(avg_rmse_train, avg_rmse_test))
# f.write("Index of outliers = %s\n" %(out_ind))
#f.write("RMSE on unseen data = %f\n" %(rmse_un))
f.write("\n")
f.close()
