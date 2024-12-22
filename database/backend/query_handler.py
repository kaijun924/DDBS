from functools import wraps
from service_mongo.table_handler import UserTableHandler, ArticleTableHandler, ReadTableHandler, BeReadTableHandler, PopularRankTableHandler
from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler



class UnifiedHandler():
    def __init__(self):
        self.mongo_handler = MongoDBHandler(host='localhost', port=60000)
        self.redis_handler = RedisHandler(host='localhost', port=6379)
        self.hadoop_handler = HadoopHandler(hdfs_url='http://localhost:9870', hdfs_dir='articles/')
    
    def fetch_data_with_cache(self, cache_type, id, fetch_function, *args, **kwargs):
        """Fetch data with Redis caching."""
        data = self.redis_handler.get(cache_type, id)
        if data:
            # print("Cache hit")
            return data
        else:
            # print("Cache miss")
            data = fetch_function(*args, **kwargs)
            self.redis_handler.set(cache_type, id, data)
            return data
        
def cache_with_redis(redis_handler, cache_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Construct the cache key based on the function and arguments
            # cache_key = f"{func.__name__}:{':'.join(map(str, args))}"
            cached_result = redis_handler.get(cache_type, cache_key)
            if cached_result:
                print("Cache hit")
                return cached_result
            print("Cache miss")
            result = func(*args, **kwargs)
            redis_handler.set(cache_type, cache_key, result)
            return result
        return wrapper
    return decorator

class QueryHandeler():
    def __init__(self, unfidedHandler: UnifiedHandler):
        self.userTableHandler = UserTableHandler(unfidedHandler.mongo_handler)
        self.articleTableHandler = ArticleTableHandler(unfidedHandler.mongo_handler)
        self.readTableHandler = ReadTableHandler(unfidedHandler.mongo_handler)
        self.beReadTableHandler = BeReadTableHandler(unfidedHandler.mongo_handler)
        self.popularRankTableHandler = PopularRankTableHandler(unfidedHandler.mongo_handler)
        self.unfidedHandler = unfidedHandler
        
    def try_cache(self, cache_type, id, fetch_function, *args, **kwargs):
        return self.unfidedHandler.fetch_data_with_cache(cache_type, id, fetch_function, *args, **kwargs)

    def fetch_users(self, conditions={}, count=100, offset=0):
        return self.userTableHandler.fetch_users(conditions, count, offset)
    
    def fetch_user_by_id(self, uid: str):
        result_from_redis = self.redisHandler.get("u"+uid, 'user')
        if result_from_redis:
            print("cache hit")
            return result_from_redis
        else:
            result_from_mongo = self.userTableHandler.fetch_users({"uid": uid})
            self.redisHandler.set("u"+uid, 'user', result_from_mongo)
            return result_from_mongo
    
    def fetch_users_by_region(self, region: str, count=100, offset=0):
        return self.userTableHandler.fetch_users_by_region(region, count, offset)
    
    def fetch_articles(self, conditions={}, count=100, offset=0):
        return self.articleTableHandler.fetch_articles(conditions, count, offset)
    
    def fetch_article_by_id(self, aid: str):
        result_from_redis = self.redisHandler.get("a"+aid, 'article')
        if result_from_redis:
            print("cache hit")
            return result_from_redis
        else:
            result_from_mongo = self.articleTableHandler.fetch_articles({"aid": aid})
            self.redisHandler.set("a"+aid, 'article', result_from_mongo)
            return result_from_mongo
    
    def fetch_articles_by_category(self, category: str, count=100, offset=0):
        return self.articleTableHandler.fetch_articles_by_category(category, count, offset)
    
    def fetch_reads(self, conditions={}, count=100, offset=0):
        return self.readTableHandler.fetch_reads(conditions, count, offset)
    
    def fetch_reads_by_id(self, bid: str):
        result_from_redis = self.redisHandler.get("r"+bid, 'read')
        if result_from_redis:
            print("cache hit")
            return result_from_redis
        else:
            result_from_mongo = self.readTableHandler.fetch_reads({"id": "r"+bid})
            self.redisHandler.set("r"+bid, 'read', result_from_mongo)
            return result_from_mongo
    
    def fetch_user_read(self, uid: str):
        user = self.userTableHandler.fetch_users({"uid": uid})
        reads = self.readTableHandler.fetch_reads_by_user(uid)   
        return {
            "user": user,
            "reads": reads
        }
    
    def fetch_beReads(self, conditions={}, count=100, offset=0):
        return self.beReadTableHandler.fetch_beReads(conditions, count, offset)
    
    def fetch_beRead_by_id(self, brid: str):
        result_from_redis = self.redisHandler.get("br"+brid, 'beRead')
        if result_from_redis:
            print("cache hit")
            return result_from_redis
        else:
            result_from_mongo = self.beReadTableHandler.fetch_beReads({"id": "br"+brid})
            self.redisHandler.set("br"+brid, 'beRead', result_from_mongo)
            return result_from_mongo
    
    def fetch_popularRanks(self, conditions={}, count=100, offset=0):
        return self.popularRankTableHandler.fetch_popularRanks(conditions, count, offset)
    
    def fetch_popularRank_by_id(self, id: int):
        result_from_redis = self.redisHandler.get(str(id), 'popularRank')
        if result_from_redis:
            print("cache hit")
            return result_from_redis
        else:
            result_from_mongo = self.popularRankTableHandler.fetch_popularRanks({"id": id})
            self.redisHandler.set(str(id), 'popularRank', result_from_mongo)
            return result_from_mongo
        
    def fetch_article_content_by_id(self, id: int):
        return self.hadoopHandler.read_file(id)
        