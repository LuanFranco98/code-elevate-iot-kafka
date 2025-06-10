import os
import redis
import json

class RedisClient:
    def __init__(self):
        self.redis_client = self.get_redis_client()


    def get_redis_client(self):
        redis_client = None
        try:
            redis_client = redis.Redis(
                host=os.environ["REDIS_HOST"],
                port=os.environ["REDIS_PORT"],
                db=0
            )
            redis_client.ping()  # Test connection
            print("Successfully connected to Redis.")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            raise ConnectionError(f"Failed to connect to Redis: {e}") from e
        
        return redis_client


    def save_to_redis(self, data):
        try:
            key = f"sensor:{data['sensor_id']}"
            self.redis_client.set(key, json.dumps(data))
            print(f"Saved to Redis: {key}")
        except Exception as e:
            print(f"Error saving to Redis: {e}")
            raise e