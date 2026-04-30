-- Count total data
SELECT COUNT(*) FROM sensor_data_virtual;

-- View sample data
SELECT * FROM sensor_data_virtual LIMIT 5;

-- Extract moisture (example)
SELECT payload::json->>'Moisture Meter - moisture'
FROM sensor_data_virtual
LIMIT 10;

-- Moisture
SELECT AVG((payload::json->>'Moisture Meter - moisture')::float) AS avg_moisture
FROM sensor_data_virtual;

-- water_usage
SELECT AVG((payload::json->>'water_usage')::float) AS avg_water
FROM sensor_data_virtual;

-- Electricity usage
SELECT AVG((payload::json->>'current')::float) AS avg_energy
FROM sensor_data_virtual;
