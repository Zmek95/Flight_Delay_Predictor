-- Extract data before feture engineering

-- Flights
-- Extract data before feture engineering

-- Flights Train data set
\copy (SELECT fl_date, mkt_unique_carrier, branded_code_share, mkt_carrier, mkt_carrier_fl_num, op_unique_carrier, tail_num, op_carrier_fl_num, origin_airport_id, origin, origin_city_name, dest_airport_id, dest, dest_city_name, crs_dep_time, crs_arr_time, dup, crs_elapsed_time, flights, distance, date_part('year', TO_DATE(fl_date,'YYYY-MM-DD')) as year, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month, date_part('day', TO_DATE(fl_date,'YYYY-MM-DD')) as day, date_part('dow', TO_DATE(fl_date,'YYYY-MM-DD')) as day_of_week, date_part('week', TO_DATE(fl_date,'YYYY-MM-DD')) as week_of_year, crs_dep_time / 100 as crs_dep_hour, crs_arr_time / 100 as crs_arr_hour, arr_delay FROM flights TABLESAMPLE BERNOULLI (.06153) REPEATABLE (1)) To '../data/flights.csv' With CSV HEADER

-- Flights aggregated variables
----- variables we will not have in test

-- Day of week flight_delay_aggregate
\copy (select mkt_unique_carrier, origin_airport_id, dest_airport_id, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month, avg(arr_delay) as month_avg_arr_delay, avg(air_time) as month_avg_air_time, avg(carrier_delay) as month_avg_carrier_delay, avg(weather_delay) as month_avg_weather_delay, avg(nas_delay) as month_avg_nas_delay, avg(security_delay) as month_avg_security_delay, avg(late_aircraft_delay) as month_avg_late_aircraft_delay from flights GROUP BY mkt_unique_carrier, origin_airport_id, dest_airport_id, month) To '../data/flight_delay_aggregate_monthly.csv' With CSV HEADER


-- Day of week flight_delay_aggregate
\copy (select mkt_unique_carrier, origin_airport_id, dest_airport_id, date_part('dow', TO_DATE(fl_date,'YYYY-MM-DD')) as day_of_week, avg(arr_delay) as day_of_week_avg_arr_delay, avg(air_time) as day_of_week_avg_air_time, avg(carrier_delay) as day_of_week_avg_carrier_delay, avg(weather_delay) as day_of_week_avg_weather_delay, avg(nas_delay) as day_of_week_avg_nas_delay, avg(security_delay) as day_of_week_avg_security_delay, avg(late_aircraft_delay) as day_of_week_avg_late_aircraft_delay from flights GROUP BY mkt_unique_carrier, origin_airport_id, dest_airport_id, day_of_week) To '../data/flight_delay_aggregate_day_of_week.csv' With CSV HEADER


---
\copy (select mkt_unique_carrier, origin_airport_id, dest_airport_id, crs_arr_time / 100 AS crs_arr_hour, avg(arr_delay) as arr_hour_avg_arr_delay, avg(air_time) as arr_hour_avg_air_time, avg(carrier_delay) as arr_hour_avg_carrier_delay, avg(weather_delay) as arr_hour_avg_weather_delay, avg(nas_delay) as arr_hour_avg_nas_delay, avg(security_delay) as arr_hour_avg_security_delay, avg(late_aircraft_delay) as arr_hour_avg_late_aircraft_delay from flights GROUP BY mkt_unique_carrier, origin_airport_id, dest_airport_id, crs_arr_hour) To '../data/flight_delay_aggregate_arrive_hour.csv' With CSV HEADER

------ airport traffic
--- airport traffic
\copy (select departures.airport_id, departures.month as month, departures, arrivals, (departures + arrivals) as total_flights from (Select origin_airport_id as airport_id, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month, count(*) as departures from flights group by airport_id, month) departures join(Select dest_airport_id as airport_id, date_part('month', TO_DATE(fl_date,'YYYY-MM-DD')) as month, count(*) as arrivals from flights group by airport_id, month) arrivals on departures.airport_id=arrivals.airport_id and departures.month=arrivals.month) To '../data/flight_airport_traffic.csv' With CSV HEADER

-- Passengers

-- passengers and seats monthly
\copy (Select unique_carrier as mkt_unique_carrier, origin_airport_id, dest_airport_id, month, SUM(seats) AS month_flight_seats, SUM(passengers) AS month_flight_passengers, AVG(flight_avg_seats) AS month_flight_avg_seats, AVG(flight_avg_passengers) AS month_flight_avg_passengers from (SELECT unique_carrier, origin_airport_id, dest_airport_id, year, month, seats, passengers, case when departures_performed = 0 then 0 else seats/departures_performed end as flight_avg_seats, case when departures_performed = 0 then 0 else passengers/departures_performed end as flight_avg_passengers FROM passengers) p GROUP BY mkt_unique_carrier, origin_airport_id, dest_airport_id, month) To '../data/passengers_flight_montly_aggregate.csv' With CSV HEADER

-- Passengers - month_airline_avg_passengers
\copy (Select unique_carrier as mkt_unique_carrier, month, SUM(seats) AS carrier_month_seats, SUM(passengers) AS carrier_month_passengers, AVG(flight_avg_seats) AS carrier_month_avg_seats, AVG(flight_avg_passengers) AS carrier_month_avg_passengers from (SELECT unique_carrier, origin_airport_id, dest_airport_id, year, month, seats, passengers, case when departures_performed = 0 then 0 else seats/departures_performed end as flight_avg_seats, case when departures_performed = 0 then 0 else passengers/departures_performed end as flight_avg_passengers FROM passengers ) p GROUP BY mkt_unique_carrier, month) To '../data/passengers_carrier_monthly_aggregate.csv' With CSV HEADER


-- passengers Passengers - month_airport_avg_passengers
\copy (SELECT airport_id, month, SUM(seats) AS airport_month_flight_seats, SUM(passengers) AS airport_month_passengers FROM (SELECT origin_airport_id as airport_id, month, seats, passengers FROM passengers Union SELECT dest_airport_id as airport_id, month, seats, passengers FROM passengers) a GROUP BY airport_id, month) To '../data/passengers_airport_monthly_aggregate.csv' With CSV HEADER


-- Fuel Comsumption - aggregated data - Table ready to join with flights
-- # Fuel_comsumption aggregated data - Table ready to join with flights
\copy (select unique_carrier as mkt_unique_carrier, month, avg(tdomt_gallons) as month_avg_fuel_comsumption from fuel_comsumption group by unique_carrier, month) To '../data/fuel_comsumption_monthyl_aggregate.csv' With CSV HEADER
