from kafka import KafkaConsumer
import json

class ConsumerClass:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'iot-sensor-data',
            api_version=(3, 8, 0), # passei uma fome por cauas dessa versao aqui
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='iot-group'
        )