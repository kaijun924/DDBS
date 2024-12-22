import redis
import bson.json_util as json_util

class RedisHandler:
    """Handles Redis operations."""

    def __init__(self, host: str = 'localhost', port: int = 6379):
        """Initialize the Redis connection."""
        self.connection = self.connect(host, port)

    def connect(self, host: str, port: int):
        """Connect to Redis."""
        connection = redis.Redis(host=host, port=port, db=0)
        connection.config_set('maxmemory', '100mb')
        connection.config_set('maxmemory-policy', 'allkeys-lru')
        return connection

    def _construct_key(self, cache_type: str, id: str) -> str:
        """Construct Redis keys."""
        return f"{cache_type}_{id}"

    def set(self, cache_type: str, id: str, value):
        """Set a value in Redis."""
        query_key = self._construct_key(cache_type, id)
        value = json_util.dumps(value)
        self.connection.set(query_key, value)

    def get(self, cache_type: str, id: str):
        """Get a value from Redis."""
        query_key = self._construct_key(cache_type, id)
        if self.connection.exists(query_key):
            return json_util.loads(self.connection.get(query_key).decode('utf-8'))
        return None

    def delete(self, cache_type: str, id: str):
        """Delete a key from Redis."""
        query_key = self._construct_key(cache_type, id)
        self.connection.delete(query_key)