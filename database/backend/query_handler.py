from curses import KEY_FIND
from functools import wraps
from service_mongo.table_handler import UserTableHandler, ArticleTableHandler, ReadTableHandler, BeReadTableHandler, PopularRankTableHandler
from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler

class UnifiedHandler():
    def __init__(self):
        self.mongo_handler = MongoDBHandler(host='localhost', port=60000)
        self.redis_handler = RedisHandler(host='localhost', port=6379)
        self.hadoop_handler = HadoopHandler(hdfs_url='http://localhost:9870', hdfs_dir='/articles/')
        
        self.mongo_handler.set_redis_handler(self.redis_handler)
        self.redis_handler = self.redis_handler
    
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
        
def cache_with_redis(cache_type):
    """
    Decorator for caching with Redis, dynamically fetching the redis_handler.

    Args:
        cache_type: The type of cache (e.g., 'user', 'article', 'hadoop').
    
    Returns:
        A decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Access redis_handler dynamically from the instance (self)
            redis_handler = self.redis_handler
            
            # Construct the cache key
            cache_id = kwargs.get('id', args[0])  # Assume the first arg is the ID
            cache_key = f"{cache_type}_{cache_id}"
            
            # Try fetching from cache
            cached_result = redis_handler.get(cache_type, cache_key)
            if cached_result:
                print(f"Cache hit for {cache_key}")
                return cached_result
            
            print(f"Cache miss for {cache_key}, fetching from database")
            # Fetch the result and cache it
            result = func(self, *args, **kwargs)
            redis_handler.set(cache_type, cache_key, result)
            return result
        return wrapper
    return decorator

class QueryHandeler():
    def __init__(self, unfidedHandler: UnifiedHandler):
        # self.unfidedHandler = unfidedHandler
        self.userTableHandler = UserTableHandler(unfidedHandler.mongo_handler)
        self.articleTableHandler = ArticleTableHandler(unfidedHandler.mongo_handler)
        self.readTableHandler = ReadTableHandler(unfidedHandler.mongo_handler)
        self.beReadTableHandler = BeReadTableHandler(unfidedHandler.mongo_handler)
        self.popularRankTableHandler = PopularRankTableHandler(unfidedHandler.mongo_handler)
        
        ## for cache_with_redis decorator
        self.redis_handler = unfidedHandler.redis_handler
        
        ## hadoop
        self.hadoopHandler = unfidedHandler.hadoop_handler
        
    def bulk_insert(self, db_folder = "../db-generation/"):
        self.userTableHandler.bulk_insert(f"{db_folder}user.dat")
        self.articleTableHandler.bulk_insert(f"{db_folder}article.dat")
        self.readTableHandler.bulk_insert(f"{db_folder}read.dat")
        self.readTableHandler.clear_no_cache_map()
        self.beReadTableHandler.bulk_insert_be_read_2()
        self.popularRankTableHandler.bulk_insert_popularRank()
    
    @cache_with_redis('user')
    def fetch_user_by_id(self, uid: str):
        result = self.userTableHandler.fetch_user_by_id(uid)
        return result 
        
    def fetch_users(self, conditions={}, count=100, offset=0):
        return self.userTableHandler.fetch_users(conditions, count, offset)
    
    def fetch_users_by_region(self, region: str, count=100, offset=0):
        return self.userTableHandler.fetch_users_by_region(region, count, offset)
    
    
    @cache_with_redis('article')
    def fetch_article_by_id(self, aid: str):
        result = self.articleTableHandler.fetch_article_by_id(aid)
        return result
    
    def fetch_articles(self, conditions={}, count=100, offset=0):
        return self.articleTableHandler.fetch_articles(conditions, count, offset)

    def fetch_articles_by_category(self, category: str, count=100, offset=0):
        return self.articleTableHandler.fetch_articles_by_category(category, count, offset)
    
    
    @cache_with_redis('read')
    def fetch_reads_by_id(self, bid: str):
        # result = self.readTableHandler.fetch_reads({"id": "r"+bid})
        result = self.readTableHandler.fetch_read_by_id(bid)
        return result
    
    def fetch_reads(self, conditions={}, count=100, offset=0):
        return self.readTableHandler.fetch_reads(conditions, count, offset)
    
    def fetch_user_read(self, uid: str):
        user = self.userTableHandler.fetch_user_by_id(uid)
        reads = self.readTableHandler.fetch_reads_by_user(uid)   
        return {
            "user": user,
            "reads": reads
        }
    
    
    @cache_with_redis('beRead')
    def fetch_beRead_by_id(self, brid: str):
        result = self.beReadTableHandler.fetch_beReads({"id": "br"+brid})
        return result
    
    def fetch_beReads(self, conditions={}, count=100, offset=0):
        return self.beReadTableHandler.fetch_beReads(conditions, count, offset)
    

    @cache_with_redis('popularRank')
    def fetch_popularRank_by_id(self, condition):
        result = self.popularRankTableHandler.fetch_popularRanks(condition)
        return result
    
    def fetch_popularRanks(self, conditions={}, count=100, offset=0):
        return self.popularRankTableHandler.fetch_popularRanks(conditions, count, offset)
    
        
    # @cache_with_redis('hadoop')
    def fetch_article_content_by_id(self, id: int):
        return self.hadoopHandler.read_file(id)
    
    # # @cache_with_redis('hadoop_list')
    # def fetch_article_content_by_id(self, id: int):
    #     return self.hadoopHandler.list_files()