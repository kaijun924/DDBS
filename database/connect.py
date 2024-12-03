from pymongo import MongoClient

class Connect:
    @classmethod
    def get_connection(cls):
        return MongoClient('localhost', 60000).connect().demo