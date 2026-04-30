-- Count total data
SELECT COUNT(*) FROM sensor_data_virtual;

-- View sample data
SELECT * FROM sensor_data_virtual LIMIT 5;

-- Extract moisture (example)
SELECT payload::json->>'Moisture Meter - moisture'
FROM sensor_data_virtual
LIMIT 10;
