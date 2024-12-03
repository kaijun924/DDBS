from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne

#same like user
class Read:
    @classmethod
    def bulk_write(cls, bulk_dict):
        beijing = MongoClient('localhost', 60000).connect.demo.read_beijing
        hong_kong = MongoClient('localhost', 60000).connect.demo.read_hongkong
        beijing.bulk_write(bulk_dict['Beijing'], ordered=True)
        hong_kong.bulk_write(bulk_dict['Hong Kong'], ordered=True)