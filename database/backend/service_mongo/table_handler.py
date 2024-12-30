import json
from pymongo import MongoClient, errors
from .handler_tools import BeReadTools, ReadTime, DateToTimestamp
from utils.helpers import handle_exceptions, log_execution_time
from .handler import MongoDBHandler
import time
from functools import wraps

class TableHandler:
    """Base class for handling common database operations."""    
    def __init__(self, collection, cache_handler=None):
        """Initialize with a MongoDB collection."""
        self.collection = collection
        self.cache_handler = cache_handler
        
    def set_cache_handler(self, cache_handler):
        self.cache_handler = cache_handler
    
    @handle_exceptions
    @log_execution_time
    def bulk_insert(self, json_file: str, batch_size: int = 5000):
        """
        Bulk inserts data from a JSON file into the MongoDB collection.
        Uses the duplication_logic method for optional record transformation.
        """
        with open(json_file, 'r', encoding='utf-8') as file:
            buffer = []
            count = 0
            for line in file:
                record = json.loads(line)
                # Apply duplication logic (can be overridden in subclasses)
                records = self._process_record(record)
                buffer.extend(records)
                count += 1
                # Bulk write when buffer reaches batch_size
                if len(buffer) >= batch_size:
                    self._write_to_db(buffer)
                    buffer = []
            # Final flush of any remaining records
            if buffer:
                self._write_to_db(buffer)
        print(f"Finished processing {count} records.")

    def _process_record(self, record):
        """
        Default process record logic: No special handling.
        Override this method in subclasses for custom logic.
        """
        return [record]
    
    def _write_to_db(self, data):
        """Write data to the specified collection."""
        try:
            result = self.collection.insert_many(data, ordered=False)
            print(f"\t Inserted {len(result.inserted_ids)} records into {self.collection.name}")
        except errors.BulkWriteError as e:
            print(f"Error during bulk insert: {e.details}")
        
def with_cache(cache_type):
    """
    Decorator for handling cache lookup and fallback for database operations.

    Args:
        cache_type (str): Type of cache (e.g., 'user', 'region').
    
    Returns:
        A decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self: TableHandler, *args, **kwargs):
            # Skip caching if cache_handler is not set
            if not hasattr(self, 'cache_handler') or self.cache_handler is None:
                print("Cache handler is not set. Skipping cache.")
                return func(self, *args, **kwargs)

            # Construct the cache key
            cache_key = f"{cache_type}_{args[0]}"  # Assume the first argument is the key
            cached_result = self.cache_handler.get(cache_type, cache_key)

            # Return cached result if available
            if cached_result:
                print(f"Cache hit for {cache_key}")
                return cached_result

            print(f"Cache miss for {cache_key}, invoking the function")
            # Fetch result, cache it, and return
            result = func(self, *args, **kwargs)
            self.cache_handler.set(cache_type, cache_key, result)
            return result
        return wrapper
    return decorator

class UserTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.user_collection, db_handler.redis_handler)
        self.no_cache_map = {}
            
    
    @with_cache('user')
    def fetch_user_by_id(self, uid: str):
        return self.collection.find_one({"uid": uid}, { "_id": 0, "timestamp": 0, "id": 0 })
    
    def get_region_by_uid_no_cache(self, uid):
        if uid in self.no_cache_map:
            return self.no_cache_map[uid]
        user = self.collection.find_one({"uid": uid}, { "_id": 0, "timestamp": 0, "id": 0 })
        self.no_cache_map[uid] = user.get("region")
        return user.get("region")
    
    def clear_no_cache_map(self):
        self.no_cache_map = {}

    def get_region_by_uid(self, uid):
        user = self.fetch_user_by_id(uid)
        return user.get("region")
    
    def fetch_users(self, conditions={}, count=100, offset=0):
        if count == None:
            users = self.collection.find(conditions, { "_id": 0, "timestamp": 0, "id": 0 }).sort([("timestamp", 1)])
        else:
            users = self.collection.find(conditions, { "_id": 0, "timestamp": 0, "id": 0 }).sort([("timestamp", 1)]).skip(offset).limit(count)
        return list(users)
    
    def fetch_users_by_region(self, region: str, count=100, offset=0):
        return self.fetch_users({"region": region}, count, offset)

class ArticleTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.article_collection, db_handler.redis_handler)

    def _process_record(self, record):
        if record.get("category") == "science":
            r1 = record.copy()
            r2 = record.copy()
            r1["shardCopy"] = 1
            r2["shardCopy"] = 2
            return [r1, r2]
        return [record]
    
    @with_cache('article')
    def fetch_article_by_id(self, aid: str):
        return self.collection.find_one({"aid": aid}, { "_id": 0, "timestamp": 0, "id": 0 })
    
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
            }, 
            {
                "$project": {
                    "_id": 0,
                    "shardCopy": 0,
                }
            }
        ]
        if count != None:
            pipeline.append({"$skip": offset})
            pipeline.append({"$limit": count})
            
        articles = list(self.collection.aggregate(pipeline))
        return articles
    
    def fetch_article_for_beread(self, conditions={},offset=0):
        fields = {
                    "_id": 0,
                    # "timestamp": 0,
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
        super().__init__(db_handler.read_collection, db_handler.redis_handler)
        self.userTableHandler = UserTableHandler(db_handler)
        
    def _process_record(self, record):
        ##初始化不要用cache
        region = self.userTableHandler.get_region_by_uid_no_cache(record['uid'])
        record['region'] = region
        record['rid'] = record['id'].replace("r", "")
        return [record]
    
    def clear_no_cache_map(self):
        self.userTableHandler.clear_no_cache_map()

    @with_cache('read')
    def fetch_read_by_id(self, rid: str):
        result = self.collection.find_one({"rid": rid}, { "_id": 0, "timestamp": 0, "uid": 0, "region": 0 })
        return result 

    def fetch_reads(self, conditions={}, count=100, offset=0):
        ### implementation: read with added region field, which is the shard key
        ### time check, when feaching beijing user's reads. 
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
    
    def fetch_reads_to_beread(self, conditions={}, count=100, offset=0):
        ### time check, when feaching beijing user's reads. 
        ### implementation: read with added region field, which is the shard key
        fields = {
                    "_id": 0,
                    "timestamp": 0
                    # "region": 0
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
    
    @with_cache('read_by_user')
    def fetch_reads_by_user(self, uid: int):
        return self.fetch_reads({"uid": uid}, None, None)
    
    # @with_cache('read_by_article')
    def agg_reads_by_article(self):
        pipeline = [
            {"$group": {
                "_id": "$aid",  # Group all matching documents
                "readNum": {"$sum": 1},  # Total count of reads
                "readUidList": {"$addToSet": "$uid"},  # Unique list of UIDs who read

                # Comment aggregations
                "commentNum": {
                    "$sum": {"$cond": [{"$eq": ["$commentOrNot", "1"]}, 1, 0]}
                },
                "commentUidList": {
                    "$addToSet": {
                        "$cond": [{"$eq": ["$commentOrNot", "1"]}, "$uid", None]
                    }
                },

                # Agree aggregations
                "agreeNum": {
                    "$sum": {"$cond": [{"$eq": ["$agreeOrNot", "1"]}, 1, 0]}
                },
                "agreeUidList": {
                    "$addToSet": {
                        "$cond": [{"$eq": ["$agreeOrNot", "1"]}, "$uid", None]
                    }
                },

                # Share aggregations
                "shareNum": {
                    "$sum": {"$cond": [{"$eq": ["$shareOrNot", "1"]}, 1, 0]}
                },
                "shareUidList": {
                    "$addToSet": {
                        "$cond": [{"$eq": ["$shareOrNot", "1"]}, "$uid", None]
                    }
                }
            }},
            # Clean up any 'None' values in lists (optional)
            {"$project": {
                "readNum": 1,
                "readUidList": 1,
                "commentNum": 1,
                "commentUidList": {
                    "$filter": {
                        "input": "$commentUidList",
                        "as": "uid",
                        "cond": {"$ne": ["$$uid", None]}
                    }
                },
                "agreeNum": 1,
                "agreeUidList": {
                    "$filter": {
                        "input": "$agreeUidList",
                        "as": "uid",
                        "cond": {"$ne": ["$$uid", None]}
                    }
                },
                "shareNum": 1,
                "shareUidList": {
                    "$filter": {
                        "input": "$shareUidList",
                        "as": "uid",
                        "cond": {"$ne": ["$$uid", None]}
                    }
                }
            }}
        ]

        # Execute the pipeline
        results = list(self.collection.aggregate(pipeline))
        return results
    
    
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
    
    def clear(self):
        self.collection.delete_many({})

class BeReadTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.be_read_collection, db_handler.redis_handler)
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
        
        # self.readTableHandler.clear()
        reads = self.readTableHandler.fetch_reads_to_beread({}, None, None)
        # print(f"Processing {len(reads)} records.")
        # exit()
        # print(self.readTableHandler.fetch_read_by_id("10"))
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


    @handle_exceptions
    @log_execution_time
    def bulk_insert_be_read_2(self, batch_size = 1000):
        articles = self.articleTableHandler.fetch_articles({}, None, None)
        be_read_agg = self.readTableHandler.agg_reads_by_article()
        be_read_agg = {br["_id"]: br for br in be_read_agg}
        
        def article_to_be_read(article):
            be_read_entity = {}
            be_read_entity["id"] = "br" + article["aid"]
            be_read_entity["timestamp"] = article["timestamp"]
            be_read_entity["category"] = article["category"]
            be_read_entity["aid"] = article["aid"]
            
            if article["aid"] in be_read_agg:
                br = be_read_agg[article["aid"]]
                be_read_entity["readNum"] = br["readNum"]
                be_read_entity["readUidList"] = br["readUidList"]
                be_read_entity["commentNum"] = br["commentNum"]
                be_read_entity["commentUidList"] = br["commentUidList"]
                be_read_entity["agreeNum"] = br["agreeNum"]
                be_read_entity["agreeUidList"] = br["agreeUidList"]
                be_read_entity["shareNum"] = br["shareNum"]
                be_read_entity["shareUidList"] = br["shareUidList"]
            else:
                be_read_entity["readNum"] = 0
                be_read_entity["readUidList"] = []
                be_read_entity["commentNum"] = 0
                be_read_entity["commentUidList"] = []
                be_read_entity["agreeNum"] = 0
                be_read_entity["agreeUidList"] = []
                be_read_entity["shareNum"] = 0
                be_read_entity["shareUidList"] = []
            
            return be_read_entity
        
        be_read_list = list(map(article_to_be_read, articles))
        print(f"Found {len(be_read_list)} articles.")
        
        
        count = 0
        buffer = []
        for be_read in be_read_list:
            if be_read.get("category") == "science":
                r1 = be_read.copy()
                r2 = be_read.copy()
                r1["shardCopy"] = 1
                r2["shardCopy"] = 2
                buffer.extend([r1, r2])
            else:
                be_read["shardCopy"] = 2
                buffer.append(be_read)
            count += 1
            if len(buffer) >= batch_size:
                self._write_to_db(buffer)
                buffer = []
        if buffer:
            self._write_to_db(buffer)
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
            },
            {
                "$project": {
                    "_id": 0,
                    # "shardCopy": 0,
                }
            }
        ]
        if count != None:
            pipeline.append({"$skip": offset})
            pipeline.append({"$limit": count})

        beread = self.collection.aggregate(pipeline)
        return list(beread)[0]


"""
id, timestamp, temporalGranularity, articleAidList
"""
class PopularRankTableHandler(TableHandler):
    def __init__(self, db_handler: MongoDBHandler):
        super().__init__(db_handler.popular_rank_collection, db_handler.redis_handler)
        self.readTableHandler = ReadTableHandler(db_handler)

    @handle_exceptions
    @log_execution_time
    def bulk_insert_popularRank(self, batch_size = 5000):
        #获取read表的所有数据
        reads = self.readTableHandler.fetch_read_for_popular_rank({}, None, None)

        time_reads = {'daily': {}, 'weekly': {}, 'monthly': {}}
        count = 0
        for read in reads:
            aid = read['aid']
            t = ReadTime(read['timestamp'])
            count += 1
            if count % batch_size == 0:
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
        # pipeline = [
        #     {
        #         "$match": conditions
        #     },
        #     {
        #         "$group": {
        #             "temporalGranularity": "$temporalGranularity",  # Group by the unique identifier
        #         }
        #     },
        #     {
        #         "$replaceRoot": { "newRoot": "$deduplicatedDoc" }
        #     },
        #     {
        #         "$project": {
        #             "_id": 0,
        #         }
        #     }
        # ]
        # if count != None:
        #     pipeline.append({"$skip": offset})
        #     pipeline.append({"$limit": count})

        # popularRanks = self.collection.aggregate(pipeline)
        fields = {
                    "_id": 0
                }
        popularRanks = self.collection.find(conditions,fields)
        return list(popularRanks)


    