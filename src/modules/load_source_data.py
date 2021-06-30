import pandas as pd
import numpy as np

def load_data_set(path= './data', file= 'flights.csv', test=False):
    '''
    Load Train or Test data add new features from database. 

    Parameters
    ----------
    Path : str, Location of source file. Ex. './data'.
    
    file : str, Name of file, include extension .
        Target vector relative to X.
    
    test: boolean, default=False
        True loads test. False loads train data.
           
    Returns
    -------
    X : pandas DataFrame
        DataFrame containing training or test data. 
    
    y : pandas Series (Only for training data)
        If test = False it returns a target variable in pandas Series.
    '''
    # Load Train or Test csv
    X = pd.read_csv(f'{path}/{file}', low_memory=False)
    if test:
        return X
    else:
    # Take target variable out of flights data set
        # Remove rows where Target variable is null
        X = X[X['arr_delay'].notna()]
        
        y = X['arr_delay']
        X = X.drop(['arr_delay'], axis=1)
        return X, y
 

def load_agg_data(X, path= './data', test=False):
    '''
    Add aggregated variables as new features to Train or Test data set. 

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

    # Load flights aggregate data
    flight_delay_aggregate_mth = pd.read_csv(f'{path}/flight_delay_aggregate_monthly.csv')
    flight_delay_aggregate_dow = pd.read_csv(f'{path}/flight_delay_aggregate_day_of_week.csv')
    flight_delay_aggregate_arrive_hour= pd.read_csv(f'{path}/flight_delay_aggregate_arrive_hour.csv')
    flight_airport_traffic = pd.read_csv(f'{path}/flight_airport_traffic.csv')

    # Load passengers aggregate data
    passengers_flight_montly_aggregate = pd.read_csv(f'{path}/passengers_flight_montly_aggregate.csv')
    passengers_carrier_monthly_aggregate = pd.read_csv(f'{path}/passengers_carrier_monthly_aggregate.csv')
    passengers_airport_monthly_aggregate= pd.read_csv(f'{path}/passengers_airport_monthly_aggregate.csv')
    # Load fuel comsumption data
    fuel_comsumption_monthyl_aggregate= pd.read_csv(f'{path}/fuel_comsumption_monthyl_aggregate.csv')

    # join tables data from origin
    flights = pd.merge(X, flight_delay_aggregate_mth, how='left', on=['mkt_unique_carrier', 'origin_airport_id', 'dest_airport_id',  'month'])
    flights = pd.merge(flights, flight_delay_aggregate_dow, how='left', on=['mkt_unique_carrier', 'origin_airport_id', 'dest_airport_id',  'day_of_week'])
    flights = pd.merge(flights, flight_delay_aggregate_arrive_hour, how='left', on=['mkt_unique_carrier', 'origin_airport_id', 'dest_airport_id', 'crs_arr_hour'])

    # Join Airport traffic
    orig = flight_airport_traffic[['airport_id','month', 'total_flights']]
    orig.columns = ['origin_airport_id','month','origin_total_flights']
    dest = flight_airport_traffic[['airport_id','month','total_flights']]
    dest.columns = ['dest_airport_id','month','dest_total_flights']
    flights = pd.merge(flights, orig, how='left', on=['origin_airport_id','month'])
    flights = pd.merge(flights, dest, how='left', on=['dest_airport_id','month'])

    
    # Join Passengers data
    flights = pd.merge(flights, passengers_flight_montly_aggregate, how='left', on=['mkt_unique_carrier', 'origin_airport_id', 'dest_airport_id','month'])
    flights = pd.merge(flights, passengers_carrier_monthly_aggregate, how='left', on=['mkt_unique_carrier', 'month'])

    flights = pd.merge(flights, fuel_comsumption_monthyl_aggregate, how='left', on=['mkt_unique_carrier', 'month'])

    #Flights has origin and destination ariports. we add it from the table.
    orig_pass = passengers_airport_monthly_aggregate[['airport_id','month', 'airport_month_flight_seats', 'airport_month_passengers']]
    orig_pass.columns = ['origin_airport_id','month', 'orig_airport_month_flight_seats', 'orig_airport_month_passengers']
    dest_pass = passengers_airport_monthly_aggregate[['airport_id','month', 'airport_month_flight_seats', 'airport_month_passengers']]
    dest_pass.columns = ['dest_airport_id','month', 'dest_airport_month_flight_seats', 'dest_airport_month_passengers']

    flights = pd.merge(flights, orig_pass, how='left', on=['origin_airport_id','month'])
    flights = pd.merge(flights, dest_pass, how='left', on=['dest_airport_id','month'])
    
    return flights
