'''
Feature engineering functions
'''    

import pandas as pd  
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector, make_column_transformer



def scale_data(X):
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=list(X.columns))
    return scaler, X_scaled

def scale_encoder(X, drop_first=True):
    '''
    Feature scales all numerical features using StandardScaler()
    One-hot encodes all categorical features using OneHotEncoder()

    Parameters
    ----------
    X : pandas DataFrame.
        Train or test data with categorical variables
        
    drop_first: boolean, default=True
        returns P-1 columns for P columns, this is needed for some 
        regression models to avoid multicollinearity.

    Returns
    -------
    processed_df : pandas DataFrame
        Pandas DataFrame with numerical features scaled and
        categorical features encoded.
        
    scaler : StandardScaler object,
        This can be used to transform scaled features
        back to the orginal format.
    '''
    
    #ct = make_column_transformer((OneHotEncoder(), make_column_selector(dtype_include=object)))
    #encoded_features = np.array(ct.fit_transform(X))
    #encoded_df = pd.DataFrame(encoded_features, columns=ct.get_feature_names())
    
    cat = X.select_dtypes(include=object)
    names = list(cat.columns)
    encoded_df = pd.get_dummies(cat, prefix=names, drop_first=drop_first)
    
    X_numeric = X.select_dtypes(exclude=object)
    scaler, X_numeric = scale_data(X_numeric)
    
    processed_df = pd.concat([X_numeric, encoded_df], axis=1)
    
    return processed_df, scaler


def print_cat_describe(df):
    for col in train.dtypes[train.dtypes == 'object'].index:
        print("Variable: ", col)
        print(df[col].describe())
        print("Unique values: ", df[col].unique())
        print('')

def print_null_features(df):
    '''
    Calculates and prints total rows of a column with missing values and the Percentage of rows for that specific column. 

    Parameters
    ----------
    X : pandas DataFrame
        Test or Train dataset.
           
    Returns
    -------
    features : pandas.core.series.Series
        Pandas Series containing names of features with missing values. 

    '''
    # missing data
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    
    print("Missing data:")
    print("-------------")
    print(missing_data.head(30))
    
    return total


def num_null_replacement(df):  
    '''
    Replaces null values to all numeric features in Train or Test data set. 

    Parameters
    ----------
    X : pandas DataFrame
        Test or Train dataset.
    
    Path : str, Location of source file. Ex. './data'.
        Location of files to read and load.

    
    test: boolean, default=False
        True loads test. False loads train data.
           
    Returns
    -------
    X : pandas DataFrame
        Pandas DataFrame containing Train or Test data and additional features. 

    '''
    
    # Print missing data
    total = print_null_features(df)
    
    for feature in total[total > 0].index:
        if df[feature].dtypes != 'object':
            df[feature] = df[feature].fillna(0)
            
    print_null_features(df)
    
    return df


def get_ord_digit(x):
    '''
    Replaces alpha numeric with numeric values. Returns ascii value for letters and keeps digits 
    Used to replace tail_num
    Parameters
    ----------
    x : pandas Series
        Test or Train dataset.
           
    Returns
    -------
    X : pandas Series with numeric values
        Pandas DataFrame containing Train or Test data and additional features. 

    '''

    new = []
    
    for l in x:
        if l.isdigit():
            new.append(l)
        else:
            new.append(ord(l))

    tail_num_n = ''
    for l in new:
        tail_num_n += str(l)
        
    return int(tail_num_n)