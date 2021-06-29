

-- Flights
\copy (SELECT * , date_part('year', TO_DATE(fl_date,'YYYY-MM-DD')) as year, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month, date_part('day', TO_DATE(fl_date,'YYYY-MM-DD')) as day FROM flights TABLESAMPLE SYSTEM (.06153) REPEATABLE (1)) To '../data/flights_10k.csv' With CSV HEADER

-- Passengers
\copy (SELECT * FROM passengers WHERE ROW(unique_carrier, origin_airport_id, dest_airport_id, year, month) in (SELECT mkt_unique_carrier AS unique_carrier, origin_airport_id, dest_airport_id, date_part('year', TO_DATE(fl_date,'YYYY-MM-DD')) as year,date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month FROM flights TABLESAMPLE SYSTEM (.06153) REPEATABLE (1))) To '../data//passengers_10k.csv' With CSV HEADER

-- Fuel Comsumption
\copy (SELECT * FROM fuel_comsumption WHERE ROW(unique_carrier, year, month) in (SELECT mkt_unique_carrier AS unique_carrier,  date_part('year', TO_DATE(fl_date,'YYYY-MM-DD')) as year, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month FROM flights TABLESAMPLE SYSTEM (.06153) REPEATABLE (1))) To '../data/fuel_comsumption_10k.csv' With CSV HEADER
