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

    def publish_data(self, channel, message):
        return self.connection.publish(channel=channel, message=message)

    def create_pubsub(self):
        pubsub = self.connection.pubsub()
        return pubsub

    def subscribe_to_channel(self, channel, sub):
        return sub.subscribe(channel)

    def set_list(self, list_key, *args):
        return self.connection.lpush(list_key, args)

    def exists_key(self, list_key):
        return self.connection.exists(list_key)

    def get_list_members(self, list_key, index):
        return self.connection.lindex(list_key, index)


redis_connection = RedisConnection()
