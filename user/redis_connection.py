import redis
from iconfig import settings


class RedisConnection:
    def __init__(self):
        self.connection = self.get_redis_connection()

    def get_redis_connection(self):
        redis_config = settings.REDIS_CONFIG

        connection = redis.StrictRedis(
            host=redis_config.get("HOST", "localhost"),
            port=redis_config.get("PORT", 6379),
        )

        return connection

    def set_key(self, key, value):
        self.connection.set(key, value)

    def get_key(self, key):
        return self.connection.get(key)

    def setex_key(self, key, expire_time, value):
        return self.connection.setex(key, expire_time, value)


redis_connection = RedisConnection()

