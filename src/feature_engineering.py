
def one_hot_encode(X):
    '''
    Hote encode categorical variables.

    Parameters
    ----------
    X : pandas DataFrame.
        Train or test data with categorical variables

    Returns
    -------
    df_dummy : pandas DataFrame
        Pandas DataFrame with numerical variables (0 or 1). 
    '''
    cat_feats = train.dtypes[X.dtypes == 'object'].index.tolist()
    df_dummy = pd.get_dummies(X[cat_feats])
    return df_dummy

def date_numeric(s):
    s = s.replace('-', '', regex=True).astype(int)
    return s

def print_cat_describe(df):
    for col in train.dtypes[train.dtypes == 'object'].index:
        print("Variable: ", col)
        print(df[col].describe())
        print("Unique values: ", df[col].unique())
        print('')