from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne
from base_handler import MongoDBHandler
from query_handler import QueryHandeler
from datetime import datetime
from PIL import Image
from io import BytesIO


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
# q.beReadTableHandler.bulk_insert_be_read()
# q.popularRankTableHandler.bulk_insert()

# print(q.beReadTableHandler.fetch_beReads({"aid":"0"}))
# print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "daily"}))
# print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "weekly"}))
# print(q.popularRankTableHandler.fetch_popularRanks({"temporalGranularity": "monthly"}))


"""
redis
"""
# print(q.fetch_user_by_id("10"))
# print(q.fetch_article_by_id("203"))
# print(q.fetch_reads_by_id("10"))
# print(q.fetch_beRead_by_id("10"))
# print(q.fetch_popularRank_by_id(10))


"""
hadoop
"""
# contents = q.fetch_article_content_by_id(1)
# print(contents.keys())
# for key in contents.keys():
#     if key.endswith('.jpg'):
#         img = Image.open(BytesIO(contents[key]))
#         img.save(f'./{key}')
#         print(f'Image {key} saved')
#     else:
#         print(contents[key].decode())