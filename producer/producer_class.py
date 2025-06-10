from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

class Producer():
    def __init__(self):    
        self.fake = Faker()
        self.producer = self.define_producer()
        self.TOPIC = "iot-sensor-data"

    def define_producer(self):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                api_version=(3, 8, 0),
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8'),

                enable_idempotence=True,
                acks='all', 
                retries=1,
                max_in_flight_requests_per_connection=1,
            )
            return producer
        except Exception as e:
            print(f"Failed to define Producer. Error:{e}")

    def generate_single_sensor_data(self):
        try:
            fake_data = {
                "ping_id": self.fake.uuid4(),
                "sensor_id": self.fake.uuid4(),
                "timestamp": self.fake.iso8601(),
                "temperature": round(random.uniform(15.0, 35.0), 2),
                "humidity": round(random.uniform(30.0, 90.0), 2),
                "location": self.fake.city()
            }
            return fake_data
        except Exception as e:
            print(f"Failed to generate sensor data. Error {e}")

    def generate_data(self):
        while True:
            data = self.generate_single_sensor_data()
            self.producer.send(self.TOPIC,key=data["sensor_id"], value=data)
            print(f"Sent: {data}")
            time.sleep(1)
