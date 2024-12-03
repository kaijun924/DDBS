import pandas as pd
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne
# from mongodb.query_manager import *
from user import User
# from mongodb.article import *
# from mongodb.read import *
# from mongodb.be_read import *
# from mongodb.popular_rank import *
import numpy as np
import json

class Init:
    def __init__(self):
        self.root_dir = '/mnt/c/Users/USER/Desktop/DDBS/db-generation/'
        self.user_path = 'user.dat'
        self.article_path = 'article.dat'
        self.read_path = 'read.dat'
        self.bulk_size = 10000
        self.bulk_size_read = 50000

    def user_bulk(self):
        print('Initializing user collection...\n')
        user_file = open(self.root_dir + self.user_path, 'r')
        bulk_dict = {'Beijing': [], 'Hong Kong': []}
        total_items = 0
        for line in user_file.readlines():
            doc = json.loads(line)
            # 可以换成insert_many？
            bulk_dict[doc['region']] += [InsertOne(doc)]
            # print(bulk_dict)

            #达到bulk_size时，写入数据库
            if total_items == self.bulk_size:
                User.bulk_write(bulk_dict)
                total_items = 0
                bulk_dict['Beijing'], bulk_dict['Hong Kong'] = [], []
            total_items += 1
        if total_items > 0:
            print("start to write")
            User.bulk_write(bulk_dict)
        user_file.close()

    def init_all(self):
        self.user_bulk()
        # self.init_article()
        # self.init_read()
        # self.init_be_read()
        # self.init_popular_rank()


if __name__ == '__main__':
    init = Init()
    init.init_all()