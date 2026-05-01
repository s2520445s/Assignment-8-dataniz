-- Query 1: Average moisture
SELECT AVG(value::float)
FROM sensor_data_virtual,
LATERAL json_each_text(payload::json) AS j(key, value)
WHERE key LIKE 'Moisture Meter%';


-- Query 2: Average water consumption
SELECT AVG(value::float)
FROM sensor_data_virtual,
LATERAL json_each_text(payload::json) AS j(key, value)
WHERE key LIKE 'Water Consumption Sensor%';


-- Query 3: Electricity comparison between houses
SELECT
  CASE
    WHEN payload::json->>'topic' LIKE '%barry910801%' THEN 'House A'
    WHEN payload::json->>'topic' LIKE '%maskedshifter%' THEN 'House B'
    ELSE 'Unknown'
  END AS house,
  SUM(value::float) AS total
FROM sensor_data_virtual,
LATERAL json_each_text(payload::json) AS j(key, value)
WHERE key LIKE 'Anmeter%'
GROUP BY house;
