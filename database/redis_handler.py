import numpy as np
import bson.json_util as json_util
import redis


class RedisHandler:
    """Handles Redis operations."""
    def __init__(self):
        """Initialize the Redis connection."""
        self.connection = self.connect()
        # print("Connected to Redis")
    def connect(cls):
        """Connect to Redis."""
        connection = redis.Redis(host='localhost', port=6379, db=0)
        connection.config_set('maxmemory', '100mb')
        connection.config_set('maxmemory-policy', 'allkeys-lru')
        return connection
    
    def set(self, id,type,value):
        """"
        type 为 user: uid
        type 为 article: aid
        type 为 read: bid
        type 为 beRead: brid
        type 为 popularRank: id
        """
        value = json_util.dumps(value)
        if type == 'user':
            #传进来的id是id
            query_id = id.replace('u','user_')
            self.connection.set(query_id, value)
        elif type == 'article':
            #传进来的id是id
            query_id = id.replace('a','article_')
            self.connection.set(query_id, value)
        elif type == 'read':
            #传进来的id是id
            query_id = id.replace('r','read_')
            self.connection.set(query_id, value)
        elif type == 'beRead':
            #传进来的id是id
            query_id = id.replace('br','beRead_')
            self.connection.set(query_id, value)
        elif type == 'popularRank':
            #传进来的id是id
            query_id = "popularRank_" + id
            self.connection.set(query_id, value)

    def get(self, id,type):
        if type == 'user':
            #传进来的id是id
            query_id = id.replace('u','user_')
        elif type == 'article':
            #传进来的id是id
            query_id = id.replace('a','article_')

        elif type == 'read':
            #传进来的id是id
            query_id = id.replace('r','read_')

        elif type == 'beRead':
            #传进来的id是id
            query_id = id.replace('br','beRead_')

        elif type == 'popularRank':
            #传进来的id是id
            query_id = "popularRank_" + id
        
        if self.connection.exists(query_id):
            return json_util.loads((self.connection.get(query_id)).decode('utf-8'))
        return None
        # return json_util.loads((self.connection.get(query_id)).decode('utf-8'))
    def delete(self, id,type):
        if type == 'user':
            #传进来的id是id
            query_id = id.replace('u','user_')
            self.connection.delete(query_id)
        elif type == 'article':
            #传进来的id是id
            query_id = id.replace('a','article_')
            self.connection.delete(query_id)
        elif type == 'read':
            #传进来的id是id
            query_id = id.replace('b','read_')
            self.connection.delete(query_id)
        elif type == 'beRead':
            #传进来的id是id
            query_id = id.replace('br','beRead_')
            self.connection.delete(query_id)
        elif type == 'popularRank':
            #传进来的id是id
            query_id = "popularRank_" + id
            self.connection.delete(query_id)

# cache = RedisHandler()
# cache.delete('u1','user')
# print(cache.get('u1','user'))