SELECT * FROM flights 
LIMIT 100;
--WHERE cancellation_code IS NOT NULL
--LIMIT 100;

--SELECT COUNT(fl_date) FROM flights; -- 15927485 rows
SELECT * FROM flights TABLESAMPLE BERNOULLI(0.07) -- (0.07/100) * 15927485
LIMIT 10000;

--SELECT * FROM flights LIMIT 10000;

-- Airport codes are in IATA format
-- test for airport with different code for FAA and IATA
SELECT * FROM flights
WHERE origin='AZA'
LIMIT 5;