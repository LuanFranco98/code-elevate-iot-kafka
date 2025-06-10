from clients import PostgresClient, RedisClient
from kafka import KafkaConsumer
import json


class Consumer():
    def __init__(self):
        self.consumer = self.define_consumer()
        self.postgres_client = PostgresClient()
        self.r = RedisClient()

    def define_consumer(self):
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

            self.process_message(parsed_value)

