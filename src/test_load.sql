-- Extract test data set for prediction


-- Flights_test data from Jan 1 2020 to Jan 7 2020
\copy (select date(fl_date), mkt_unique_carrier, branded_code_share, mkt_carrier, mkt_carrier_fl_num, op_unique_carrier, tail_num, op_carrier_fl_num, origin_airport_id, origin, origin_city_name, dest_airport_id, dest, dest_city_name, crs_dep_time, crs_arr_time, dup, crs_elapsed_time, flights, distance, date_part('year', fl_date) as year, date_part('month', fl_date) as month, date_part('day', fl_date) as day, date_part('dow', fl_date) as day_of_week, date_part('week', fl_date) as week_of_year,  crs_dep_time / 100 as crs_dep_hour, crs_arr_time / 100 as crs_arr_hour from flights_test where fl_date < '2020-01-08') To '../data/flights_test.csv' With CSV HEADER
