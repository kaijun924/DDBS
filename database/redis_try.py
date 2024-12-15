import numpy as np
import bson.json_util as json_util
import redis

connection = redis.Redis(host='localhost', port=6379)
# item = {"name": "test", "value": np.random.rand(3, 3)}
# item_json = json_util.dumps(item)
# connection.mset({"test": item_json})
# print(cache_res)
test = connection.mget({"test"})
test = json_util.loads(test[0].decode('utf-8'))
print(test["name"])
print(test["value"])