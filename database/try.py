from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne
from base_handler import MongoDBHandler
from query_handler import QueryHandeler
from datetime import datetime


# collection = MongoClient('localhost', 60000).connect.demo.user_beijing
# print(collection.find_one({"uid": "10"}))

#开始
host = 'localhost'
port = 60000
db_handler = MongoDBHandler(host, port)

q = QueryHandeler(db_handler)

#初始化
# q.readTableHandler.bulk_insert("./db-generation/read.dat")
# q.userTableHandler.bulk_insert("./db-generation/user.dat")
# q.articleTableHandler.bulk_insert("./db-generation/article.dat")
# q.beReadTableHandler.bulk_insert("./db-generation/article.dat")
print(q.beReadTableHandler.fetch_beReads({"aid": "0"}))
print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "daily"}))
print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "weekly"}))
print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "monthly"}))
# q.popularRankTableHandler.bulk_insert()