'''
Model training and evaluation functions
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR, LinearSVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor

# ************************************************************************************** 
#                                   MODELS:
# **************************************************************************************

def linpoly_reg(X, y, alpha=1, degree=5):
    '''
    Train Linear, Ridge, Lasso, and Polynomial regression models.

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    
    y : array-like of shape (n_samples,)
        Target vector relative to X
    
    alpha : float, default=1
        Regularization strength; must be a positive float

    degree : int, default=5
        The degree of the polynomial features
           
    Returns
    -------
    model_dict : dict
        Dictionary containing all models that have been fit on X and y. 
    '''

    # Linear
    lin_reg = LinearRegression()
    lin_reg.fit(X,y)

    # Ridge
    rdg_reg = Ridge(alpha=alpha)
    rdg_reg.fit(X,y)

    # Lasso
    las_reg = Lasso(alpha=alpha)
    las_reg.fit(X,y)

    # Polynomial
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    pol_reg = LinearRegression()
    pol_reg.fit(X_poly, y)

    model_dict = {'LinReg': lin_reg, 'RidgeReg': rdg_reg, 
                'LassoReg': las_reg, 'PolyReg': pol_reg}
    return model_dict


def svr_reg(X, y, epsilon=0.1, C=1, kernel='rbf', degree=3, coef0=0):
    '''
    Train SVR models.

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    
    y : array-like of shape (n_samples,)
        Target vector relative to X

    epsilon : float, default=0.1

    C : float, default=1

    kernel : str {‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’}, default='rbf'
        Specifies kernel type to be used for SVR

    degree : int, default=3
        Degree of the polynomial kernel function ('poly'). 
        Ignored by other kernels

    coef0 : float, default=0
        Independent term in kernel function.
        Only significant in 'poly' and 'sigmoid'

    Returns
    -------
    model_dict : dict
        Dictionary containing all models that have been fit on X and y. 
    '''

    # Linear SVR
    lin_svr_reg = LinearSVR(epsilon=epsilon, C=C)
    lin_svr_reg.fit(X,y)

    # SVR
    svr_reg = SVR(kernel=kernel, degree=degree, coef0=coef0, C=C, epsilon=epsilon)
    svr_reg.fit(X,y)

    model_dict = {'LinSVR_Reg': lin_svr_reg, 'SVR_Reg': svr_reg} 
    return model_dict

def randforest_reg(X, y, n_estimators=100, criterion='mse', max_depth=None, n_jobs=-1):
    '''
    Train random forest regressor

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    
    y : array-like of shape (n_samples,)
        Target vector relative to X
    
    n_estimators : int, default=100
        The number of trees in the forest.
    
    criterion : str {'mse', 'mae'}, default='mse'
        The function to measure the quality of the split.

    max_depth : int, default=None
        The maximum depth of a tree.

    n_jobs : int, default=-1
        The number of jobs to run in parallel.
        -1 means use all processors.
    
    Returns
    -------
    model_dict : dict
        Dictionary containing all models that have been fit on X and y. 
    '''

    rf_reg = RandomForestRegressor(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, n_jobs=n_jobs)
    rf_reg.fit(X,y)

    model_dict = {'RandomForest_Reg': rf_reg} 
    return model_dict

def gradboost_reg(X, y, loss='ls', learning_rate=0.1, n_estimators=100, max_depth=3, alpha=0.9):
    '''
    Train a gradient boost regressor

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    
    y : array-like of shape (n_samples,)
        Target vector relative to X

    loss : str {‘ls’, ‘lad’, ‘huber’, ‘quantile’}, default='ls'
        Loss funtion to be optimized 

    learning_rate : float, default=0.1
        Shrinks the contribution of each tree by learning rate.
        Trade-off between learning_rate and n_estimators

    n_estimators : int, default=100
        The number of boosting stages to perform.
        Gradient boosting is fairly robust aginst overfitting,
        so larger numbers usually result in better performance.

    max_depth : int, default=3
        Maximum depth of the individual regression estimators (trees)

    alpha : float, default=0.9
        The alpha-quantile of the huber loss function and the quantile loss function.
        Only if loss='huber' or loss='quantile'
    
    Returns
    -------
    model_dict : dict
        Dictionary containing all models that have been fit on X and y. 
    '''

    gd_reg = GradientBoostingRegressor(loss=loss, learning_rate=learning_rate, n_estimators=n_estimators
                                        , max_depth=max_depth, alpha=alpha)
    gd_reg.fit(X, y)

    model_dict = {'GradientBoost_Reg': gd_reg} 
    return model_dict

def xgboost_reg(X, y, n_estimators=100, max_depth=6, learning_rate=0.3, gamma=0, reg_lambda=1, reg_alpha=0):
    '''
    Train a XGBoost regressor

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    
    y : array-like of shape (n_samples,)
        Target vector relative to X

    n_estimators : int, default=100
        The number of boosting stages to perform.
    
    max_depth : int, default=6
        Maximum depth of the individual regression estimators (trees).

    learning_rate : float, default=0.3
        Step size shrinkage used in update to prevent overfitting.
        range: [0,1]

    gamma : float, default=0
        Minimum loss reduction required to make a further partition on a leaf node of the tree.
        The larger gamma is, the more conservative the algorithm will be.

    reg_lambda : float, default=1
        L2 regularization term on weights. Increasing this value will make model more conservative.

    reg_alpha : float, default=0
        L1 regularization term on weights. Increasing this value will make model more conservative.

    Returns
    -------
    model_dict : dict
        Dictionary containing all models that have been fit on X and y. 
    '''

    xgb_reg = XGBRegressor(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate
                            , gamma=gamma, reg_lambda=reg_lambda, reg_alpha=reg_alpha)
    xgb_reg.fit(X,y)

    model_dict = {'XGBoost_Reg': xgb_reg} 
    return model_dict

# ************************************************************************************** 
#                                   METRICS:
# **************************************************************************************

def Adjusted_R2(R2, X):
    '''
    Calculates Adjusted R2 score.

    Parameters
    ----------
    R2 : float, R2 score from a regression model that was trained on X

    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    '''
    
    n = X.shape[0]
    p = X.shape[1]
    return 1-(1-R2)*(n-1)/(n-p-1)

def regmodel_evaluation(model_dict, X_test, y_test):
    '''
    Prints several regression metrics for all the models passed to the function.

    Parameters
    ----------
    model_dict : dict, contains all regression models that have been fit on training data
        relative to X_test and y_test.

    X_test : {array-like, sparse matrix} of shape (n_samples, n_features)
        Testing vector, where n_samples in the number of samples and
        n_features is the number of features.

    y_test : array-like of shape (n_samples,)
        Target vector relative to X_test
    '''
    
    for key, value in model_dict.items():
        
        y_pred = value.predict(X_test)
        
        #metrics
        R2 = r2_score(y_test, y_pred)
        Adj_R2 = Adjusted_R2(R2, X_test)
        RMSE = mean_squared_error(y_test, y_pred, squared=False)
        
        print(f"{key} metrics:\n\tR2 = {R2}\n\tAdjusted R2 = {Adj_R2}\n\tRMSE = {RMSE}\n")
        print("*******************************************************************\n")

def ensemble_feature_importance(model, X):
    '''
    Plots feature impoetances for ensemble models in a bar graph

    Parameters
    ----------
    model : ensemble object, Trained model of an ensemble algorithm.

    X : {array-like, sparse matrix} of shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.
    '''
    
    feature_imp = pd.Series(model.feature_importances_,index=X.columns).sort_values(ascending=False)
    feature_imp = feature_imp[feature_imp > 0.01]
    
    plt.rcParams['figure.figsize'] = 20, 25
    # Creating a bar plot
    sns.barplot(x=feature_imp, y=feature_imp.index)
    
    # Add labels to your graph
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Visualizing Important Features")
    plt.show()
