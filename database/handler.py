from base_handler import MongoDBHandler, TableHandler, handle_exceptions, log_execution_time
from handler_tools import BeReadTools, ReadTime, DateToTimestamp
import time
cache = {}

class UserTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.user_collection)
        
    def get_region_by_uid(self, uid):
        if uid in cache:
            return cache[uid]
        else:
            user = self.collection.find_one({"uid": uid})
            cache[uid] = user.get("region") if user else None
        return cache[uid]
    
    def fetch_users(self, conditions={}, count=100, offset=0):
        if count == None:
            users = self.collection.find(conditions, { "_id": 0, "timestamp": 0, "id": 0 })
        else:
            users = self.collection.find(conditions, { "_id": 0, "timestamp": 0, "id": 0 }).skip(offset).limit(count)
        return list(users)
    
    def fetch_users_by_region(self, region: str, count=100, offset=0):
        return self.fetch_users({"region": region}, count, offset)

class ArticleTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.article_collection)

    def _process_record(self, record):
        if record.get("category") == "science":
            r1 = record.copy()
            r2 = record.copy()
            r1["shardCopy"] = 1
            r2["shardCopy"] = 2
            return [r1, r2]
        return [record]
    
    def fetch_articles(self, conditions={}, count=100, offset=0):
        pipeline = [
            {
                "$match": conditions
            },
            {
                "$group": {
                    "_id": "$aid",  # Group by the unique identifier
                    "deduplicatedDoc": { "$first": "$$ROOT" }
                }
            },
            {
                "$replaceRoot": { "newRoot": "$deduplicatedDoc" }
            }
        ]
        if count != None:
            pipeline.append({"$skip": offset})
            pipeline.append({"$limit": count})

        articles = self.collection.aggregate(pipeline)
        return list(articles)
    
    def fetch_article_for_beread(self, conditions={},offset=0):
        fields = {
                    "_id": 0,
                    "timestamp": 0,
                    "title": 0,
                    "abstract": 0,
                    "articleTags": 0,
                    "authors": 0,
                    "language": 0,
                    "text": 0,
                    "image": 0,
                }
        articles = self.collection.find(conditions, fields).skip(offset)
        return list(articles)
    
    def fetch_articles_by_category(self, category: str, count=100, offset=0):
        return self.fetch_articles({"category": category}, count, offset)
    
class ReadTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.read_collection)
        self.userTableHandler = UserTableHandler(db_handler)
        
    def _process_record(self, record):
        region = self.userTableHandler.get_region_by_uid(record['uid'])
        record['region'] = region
        return [record]

    def fetch_reads(self, conditions={}, count=100, offset=0):
        ### time check, when feaching beijing user's reads. 
        ### implementation: read with added region field, which is the shard key
        fields = {
                    "_id": 0,
                    "timestamp": 0,
                    "uid": 0,
                    "region": 0
                }
        if count == None:
            reads = self.collection.find(conditions, fields)
        else:
            reads = self.collection.find(conditions, fields).skip(offset).limit(count)
        return list(reads)
    
    def fetch_reads_to_beread(self, conditions={}, count=100, offset=0):
        ### time check, when feaching beijing user's reads. 
        ### implementation: read with added region field, which is the shard key
        fields = {
                    "_id": 0,
                    "timestamp": 0,
                    "region": 0
                }
        if count == None:
            reads = self.collection.find(conditions, fields)
        else:
            reads = self.collection.find(conditions, fields).skip(offset).limit(count)
        return list(reads)
    
    def fetch_read_for_popular_rank(self, conditions={}, count=100, offset=0):
        #需要id,aid,timestamp
        fields = {
                    "_id": 0,
                    "uid": 0,
                    "region": 0,
                    "commentOrNot": 0,
                    "agreeOrNot": 0,
                    "shareOrNot": 0,
                    "readTimeLength": 0,
                    "commentDetail": 0,
                }
        if count == None:
            reads = self.collection.find(conditions, fields)
        else:
            reads = self.collection.find(conditions, fields).skip(offset).limit(count)
        return list(reads)
    
    def fetch_reads_by_user(self, uid: int):
        return self.fetch_reads({"uid": uid}, None, None)
    
    
    def fetch_aggregated_reads_by_category(self, category: str):
        limit = 10
        """
        Aggregate reads for a specific article category.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "articleDatabase.Article",
                    "localField": "aid",
                    "foreignField": "aid",
                    "as": "article_details",
                }
            },
            {"$unwind": "$article_details"},  # Flatten the article details array
            {"$match": {"article_details.category": category}},  # Filter condition
            {"$group": {"_id": "$uid", "total_reads": {"$sum": 1}}},  # Group by user
            {"$limit": limit},
        ]
        return list(self.collection.aggregate(pipeline))
    
    def fetch_reads_with_details(self):
        limit = 10
        """
        Fetch reads with user and article details.
        Simulates a join between Reads, User, and Article collections.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "articleDatabase.Article",
                    "localField": "aid",
                    "foreignField": "aid",
                    "as": "article_details",
                }
            },
            {
                "$lookup": {
                    "from": "userDatabase.User",
                    "localField": "uid",
                    "foreignField": "uid",
                    "as": "user_details",
                }
            },
            {"$limit": limit},
        ]
        return list(self.collection.aggregate(pipeline))

class BeReadTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.be_read_collection)
        # self.userTableHandler = UserTableHandler(db_handler)
        self.readTableHandler = ReadTableHandler(db_handler)
        self.articleTableHandler = ArticleTableHandler(db_handler)
        self.tools = BeReadTools()
    
    def _process_record(self, record):
        return self.tools._get_beRead_by_aid(record,self.readTableHandler)
    
    def insert_new(self, record):
        record = self.tools._get_beRead_by_aid(record,self.readTableHandler)
        self.collection.insert_many(record) #
    
    ##或许可以重写bulk_insert
    @handle_exceptions
    @log_execution_time
    def bulk_insert_be_read(self, batch_size = 5000):
        articles = self.articleTableHandler.fetch_article_for_beread({}, 0)
        buffer = []
        mapping = {}
        for article in articles:
            be_read_entity = {}
            be_read_entity["id"] = "br" + article["aid"]
            be_read_entity["timestamp"] = str(time.time())
            be_read_entity["category"] = article["category"]
            be_read_entity["aid"] = article["aid"]

            mapping[article["aid"]] = len(buffer)
            buffer.append(be_read_entity)
        
        print(f"Finished processing {len(buffer)} records.")

        reads = self.readTableHandler.fetch_reads_to_beread({}, None, None)
        
        count = 0
        for read in reads:
            aid = read["aid"]
            if aid not in mapping:
                continue
            idx = mapping[aid]
            buffer[idx]["readNum"] = buffer[idx].get("readNum", 0) + 1
            buffer[idx]["readUidList"] = buffer[idx].get("readUidList", [])
            buffer[idx]["readUidList"].append(read["uid"])
            if read["commentOrNot"] == "1":
                buffer[idx]["commentNum"] = buffer[idx].get("commentNum", 0) + 1
                buffer[idx]["commentUidList"] = buffer[idx].get("commentUidList", [])
                buffer[idx]["commentUidList"].append(read["uid"])
            if read["agreeOrNot"] == "1":
                buffer[idx]["agreeNum"] = buffer[idx].get("agreeNum", 0) + 1
                buffer[idx]["agreeUidList"] = buffer[idx].get("agreeUidList", [])
                buffer[idx]["agreeUidList"].append(read["uid"])
            if read["shareOrNot"] == "1":
                buffer[idx]["shareNum"] = buffer[idx].get("shareNum", 0) + 1
                buffer[idx]["shareUidList"] = buffer[idx].get("shareUidList", [])
                buffer[idx]["shareUidList"].append(read["uid"])
            
            count += 1
            if count % 5000 == 0:
                print(f"Processing {count} records.")
        
        insert_buffer = []
        for be_read_entity in buffer:
            if be_read_entity.get("category") == "science":
                r1 = be_read_entity.copy()
                r2 = be_read_entity.copy()
                r1["shardCopy"] = 1
                r2["shardCopy"] = 2
                insert_buffer.extend([r1, r2])
            else:
                insert_buffer.append(be_read_entity)

        self.collection.insert_many(insert_buffer)
        print(f"Finished processing {count} records.")



        

    def fetch_beReads(self, conditions={}, count=100, offset=0):
        pipeline = [
            {
                "$match": conditions
            },
            {
                "$group": {
                    "_id": "$aid",  # Group by the unique identifier
                    "deduplicatedDoc": { "$first": "$$ROOT" }
                }
            },
            {
                "$replaceRoot": { "newRoot": "$deduplicatedDoc" }
            }
        ]
        if count != None:
            pipeline.append({"$skip": offset})
            pipeline.append({"$limit": count})

        beread = self.collection.aggregate(pipeline)
        return list(beread)


"""
id, timestamp, temporalGranularity, articleAidList
"""
class PopularRankTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.popular_rank_collection)
        self.readTableHandler = ReadTableHandler(db_handler)

    def bulk_insert(self, batch_size = 5000):
        #获取read表的所有数据
        reads = self.readTableHandler.fetch_read_for_popular_rank({}, None, None)

        time_reads = {'daily': {}, 'weekly': {}, 'monthly': {}}
        count = 0
        for read in reads:
            aid = read['aid']
            t = ReadTime(read['timestamp'])
            count += 1
            if count % 5000 == 0:
                print(f"Processing {count} records.")
            for temporalGranularity in time_reads.keys():
                tg = temporalGranularity

                if t.read_timestamp[tg] not in time_reads[tg]:
                    time_reads[tg][t.read_timestamp[tg]] = {}
                if aid not in time_reads[tg][t.read_timestamp[tg]]:
                    time_reads[tg][t.read_timestamp[tg]][aid] = 0
                time_reads[tg][t.read_timestamp[tg]][aid] += 1

        popid = 0
        buffer = []
        for temporalGranularity in time_reads.keys():
            for timestamp in time_reads[temporalGranularity].keys():
                tg = temporalGranularity
                timeof = timestamp

                time_reads[tg][timeof] = sorted(time_reads[tg][timeof].items(), key=lambda x: x[1], reverse=True)
                #这里只取前100个，因为太多了，可以考虑取更多
                time_reads[tg][timeof] = time_reads[tg][timeof][:100]

                popularRank_entity = {}
                popularRank_entity["id"] = popid

                if tg == "daily":
                    popularRank_entity["timestamp"] = DateToTimestamp.day_tmp(timeof)
                elif tg == "weekly":
                    popularRank_entity["timestamp"] = DateToTimestamp.week_tmp(timeof)
                elif tg == "monthly":
                    popularRank_entity["timestamp"] = DateToTimestamp.month_tmp(timeof)

                popularRank_entity["temporalGranularity"] = tg
                popularRank_entity["articleAidList"] = [aid for aid, _ in time_reads[tg][timeof]]
        
                buffer.append(popularRank_entity)

                popid += 1
            
        self.collection.insert_many(buffer)

    def fetch_popularRanks(self, conditions={}, count=100, offset=0):
        pipeline = [
            {
                "$match": conditions
            },
            {
                "$group": {
                    "_id": "$temporalGranularity",  # Group by the unique identifier
                    "deduplicatedDoc": { "$first": "$$ROOT" }
                }
            },
            {
                "$replaceRoot": { "newRoot": "$deduplicatedDoc" }
            }
        ]
        if count != None:
            pipeline.append({"$skip": offset})
            pipeline.append({"$limit": count})

        popularRanks = self.collection.aggregate(pipeline)
        return list(popularRanks)


    