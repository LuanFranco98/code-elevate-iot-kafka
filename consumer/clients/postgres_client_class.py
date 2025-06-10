import os
import psycopg2

class PostgresClient:
    def __init__(self):
        self.conn = self.get_postgres_connection()
        self.cursor = self.conn.cursor()

    def get_postgres_connection(self):
        try: 
            conn = psycopg2.connect(
                dbname=os.environ["POSTGRES_DB"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host=os.environ["POSTGRES_HOST"],
                port=5432
            )
            print("Successfully connected to PostgreSQL.")
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}") from e

        return conn

    def insert_sensor_data(self, data):
        try:
            self.cursor.execute("""
                INSERT INTO sensor_data (ping_id, sensor_id, timestamp, temperature, humidity, location)
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (ping_id) DO UPDATE
                SET 
                    sensor_id = EXCLUDED.sensor_id,
                    timestamp = EXCLUDED.timestamp,
                    temperature = EXCLUDED.temperature,
                    humidity = EXCLUDED.humidity,
                    location = EXCLUDED.location
            """, (
                data["ping_id"],
                data["sensor_id"],
                data["timestamp"],
                data["temperature"],
                data["humidity"],
                data["location"]
            ))
            self.conn.commit()
            print("Saved to PostgreSQL.")
        except Exception as e:
            print(f"Error saving to PostgreSQL: {e}")
            self.conn.rollback() 
            raise 

    def close(self):
        if self.conn:
            self.conn.close()
            print("PostgreSQL cursor closed in DataSaver.")
