from connect import Connect
from pymongo import MongoClient


class User:
    @classmethod
    def bulk_write(cls, bulk_dict):
        beijing = MongoClient('localhost', 60000).connect.demo.user_beijing
        hong_kong = MongoClient('localhost', 60000).connect.demo.user_hongkong
        beijing.bulk_write(bulk_dict['Beijing'], ordered=True)
        hong_kong.bulk_write(bulk_dict['Hong Kong'], ordered=True)
    # def delete_all(cls):
    #     beijing = Connect.get_connection().database().user_beijing
    #     hong_kong = Connect.get_connection().database().user_hongkong
    #     beijing.delete_many({})
    #     hong_kong.delete_many({})
    #     print('User collection deleted.\n')