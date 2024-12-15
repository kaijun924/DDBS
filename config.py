import pandas as pd
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne
# from mongodb.query_manager import *
from user import User
from article import Article
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

    def article_bulk(self):
        print('Initializing article collection...\n')
        article_file = open(self.root_dir + self.article_path, 'r')
        bulk_counter, bulk_dict = 0, {'science': [], 'technology': []}
        for line in article_file.readlines():
            bulk_counter += 1
            doc = json.loads(line)
            bulk_dict[doc['category']] += [InsertOne(doc)]
            if bulk_counter == self.bulk_size:
                Article.bulk_write(bulk_dict)
                bulk_counter = 0
                bulk_dict['science'], bulk_dict['technology'] = [], []
        if bulk_counter > 0:
            Article.bulk_write(bulk_dict)
        article_file.close()
    
    def read_bulk(self):
        print('Initializing read collection...\n')
        # read_file = open(self.root_dir + self.read_path, 'r')
        # bulk_counter, bulk_list, uids = 0, [], []
        # for line in read_file.readlines():
        #     bulk_counter += 1
        #     doc = json.loads(line)
        #     uids += [doc['uid']]
        #     bulk_list += [InsertOne(doc)]
        #     if bulk_counter == self.bulk_size_read:
        #         regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1}, cache=False)
        #         regions = dict(map(lambda x: (x['uid'], x['region']), regions))
        #         regions = list(map(lambda x: regions[x], uids))
        #         beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
        #         hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
        #         Read.bulk_write({'Beijing': list(np.array(bulk_list)[beijing_index]),
        #                          'Hong Kong': list(np.array(bulk_list)[hk_index])})
        #         bulk_counter, bulk_list, uids = 0, [], []
        # if bulk_counter > 0:
        #     regions = QueryManager.query_user({'uid': {'$in': uids}}, {'uid': 1, 'region': 1}, cache=False)
        #     regions = dict(map(lambda x: (x['uid'], x['region']), regions))
        #     regions = list(map(lambda x: regions[x], uids))
        #     beijing_index = np.argwhere(np.array(regions) == 'Beijing').reshape(-1)
        #     hk_index = np.argwhere(np.array(regions) == 'Hong Kong').reshape(-1)
        #     Read.bulk_write({'Beijing': list(np.array(bulk_list)[beijing_index]),
        #                      'Hong Kong': list(np.array(bulk_list)[hk_index])})


if __name__ == '__main__':
    init = Init()
    init.user_bulk()
    init.article_bulk()