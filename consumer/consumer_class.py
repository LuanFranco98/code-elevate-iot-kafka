from clients import PostgresClient, RedisClient
from kafka import KafkaConsumer
from datetime import datetime
import json
import uuid

class Consumer():
    def __init__(self):
        self.consumer = self.define_consumer()
        self.postgres_client = PostgresClient()
        self.r = RedisClient()

    def define_consumer(self):
        try:
            consumer = KafkaConsumer(
                'iot-sensor-data',
                api_version=(3, 8, 0), # passei uma fome por cauas dessa versao aqui
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='iot-group'
            )
            return consumer
        except Exception as e:
            print(f"Failed to define Consumer. Error:{e}")

    def process_message(self, msg_value):
        """
        Processes a single message, delegating saving to DataSaver.
        """
        try:
            data = msg_value
            print(f"Received: {data}")
            self.r.save_to_redis(data)
            self.postgres_client.insert_sensor_data(data)
            print("Data processing complete for this message.")
        except Exception as e:
            print(f"Failed to process message: {msg_value}. Error: {e}")
            # Optionally, implement a dead-letter queue or retry mechanism here

    def consume_messages(self):
        print("Starting message consumption...")
        for msg in self.consumer:
            # It's good practice to ensure msg.value is a dict if it comes from JSON
            if isinstance(msg.value, bytes):
                try:
                    parsed_value = json.loads(msg.value.decode('utf-8'))
                except json.JSONDecodeError:
                    print(f"Could not decode message value as JSON: {msg.value}")
                    continue
            else:
                parsed_value = msg.value # Assume it's already a dict if not bytes
            if self.is_valid(parsed_value):
                self.process_message(parsed_value)
            else:
                print("Message recieved is not valid")
                raise Exception("Message recieved is not valid")


    def is_valid(self, data: dict) -> bool:
        required_keys = {"ping_id", "sensor_id", "timestamp", "temperature", "humidity", "location"}

        if not isinstance(data, dict):
            return False

        if not required_keys.issubset(data.keys()):
            return False

        try:
            uuid.UUID(data["ping_id"])
            uuid.UUID(data["sensor_id"])
        except (ValueError, TypeError):
            return False

        try:
            # Handles ISO 8601 with or without timezone Z
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return False

        if not isinstance(data["temperature"], (int, float)):
            return False

        if not isinstance(data["humidity"], (int, float)):
            return False

        if not isinstance(data["location"], str):
            return False

        if not (15.0 <= data["temperature"] <= 35.0):
            return False

        if not (30.0 <= data["humidity"] <= 90.0):
            return False

        return True