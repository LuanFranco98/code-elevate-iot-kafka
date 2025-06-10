from consumer_class import ConsumerClass
from clients import PostgresClient, RedisClient


consumer = ConsumerClass().consumer
postgres_client = PostgresClient()
r = RedisClient()

if __name__ == '__main__':
    for msg in consumer:
        data = msg.value
        print(f"Recieved: {data}")

        r.save_to_redis(data)
        postgres_client.insert_sensor_data(data)

        print("Data Saved!")
