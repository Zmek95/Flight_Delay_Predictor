'''
Feature engineering functions
'''    

import pandas as pd  
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector 



def scale_data(X):
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=list(X.columns))
    return scaler, X_scaled

def scale_encoder(X):
    '''
    Feature scales all numerical features using StandardScaler()
    One-hot encodes all categorical features using OneHotEncoder()

    Parameters
    ----------
    X : pandas DataFrame.
        Train or test data with categorical variables

    Returns
    -------
    processed_df : pandas DataFrame
        Pandas DataFrame with numerical features scaled and
        categorical features encoded.
        
    ct : ColumnTransformer object,
        This can be used to transform one hot encoded features
        back to the orginal format.
        
    scaler : StandardScaler object,
        This can be used to transform scaled features
        back to the orginal format.
    '''
    
    ct = ColumnTransformer(transformers=[('scaler', OneHotEncoder(), make_column_selector(dtype_include=object))])
    encoded_features = np.array(ct.fit_transform(X))
    encoded_df = pd.DataFrame(encoded_features, columns=ct.get_feature_names())
    
    X_numeric = X.select_dtypes(exclude=object)
    scaler, X_numeric = scale_data(X_numeric)
    
    processed_df = pd.concat([X_numeric, encoded_df], axis=1)
    
    return processed_df, ct, scaler


def print_cat_describe(df):
    for col in train.dtypes[train.dtypes == 'object'].index:
        print("Variable: ", col)
        print(df[col].describe())
        print("Unique values: ", df[col].unique())
        print('')
