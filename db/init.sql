CREATE TABLE IF NOT EXISTS sensor_data (
    ping_id UUID PRIMARY KEY,
    sensor_id TEXT,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    location TEXT
);