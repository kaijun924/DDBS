from connect import Connect
from pymongo import MongoClient

class Article:
    @classmethod
    def bulk_write(cls, bulk_dict):
        science = MongoClient('localhost', 60000).connect.demo.article_science
        technology = MongoClient('localhost', 60000).connect.demo.article_tech

        science.bulk_write(bulk_dict['science'], ordered=True)
        technology.bulk_write(bulk_dict['technology'], ordered=True)