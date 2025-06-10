from kafka import KafkaConsumer
import psycopg2
import redis
import json
import os

# Kafka Consumer
consumer = KafkaConsumer(
    'iot-sensor-data',
    api_version=(3, 8, 0), # passei uma fome por cauas dessa versao aqui
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='iot-group'
)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=5432
)
cursor = conn.cursor()

# Redis connection
r = redis.Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    db=0
)

if __name__ == '__main__':
    for msg in consumer:
        data = msg.value
        print(f"Recieved: {data}")

        # Save to Redis
        r.set(f"sensor:{data['sensor_id']}", json.dumps(data))

        # Save to PostgreSQL
        cursor.execute("""
            INSERT INTO sensor_data (sensor_id, timestamp, temperature, humidity, location)
            VALUES (%s, %s, %s, %s, %s)
        """, (data["sensor_id"], data["timestamp"], data["temperature"], data["humidity"], data["location"]))
        conn.commit()

        print("Data Saved!")
