# IoT Data Sharing System

## Overview
This project implements an IoT data pipeline using DataNiz and NeonDB.
Sensor data from multiple devices (fridge, dishwasher, energy meter)
is streamed through an MQTT broker and stored in a relational database.

## Architecture
Devices → Broker → NeonDB

## Devices
- Fridge (moisture sensor)
- Dishwasher (water usage)
- Energy Meter (electricity usage)

## Database
Data is stored in:
sensor_data_virtual

## Example Queries
SELECT COUNT(*) FROM sensor_data_virtual;
SELECT * FROM sensor_data_virtual LIMIT 5;

## How to Run
1. Start DataNiz devices
2. Ensure NeonDB is connected
3. Run SQL queries in NeonDB

## Authors
Barry Lin
Raul Rendon
