from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne


collection = MongoClient('localhost', 60000).connect.demo.user_beijing
print(collection.find_one({"uid": "10"}))