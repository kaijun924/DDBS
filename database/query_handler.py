from base_handler import MongoDBHandler
from handler import UserTableHandler, ArticleTableHandler, ReadTableHandler, BeReadTableHandler, PopularRankTableHandler
from redis_handler import RedisHandler

class QueryHandeler():
    def __init__(self, db_handler: MongoDBHandler):
        self.userTableHandler = UserTableHandler(db_handler)
        self.articleTableHandler = ArticleTableHandler(db_handler)
        self.readTableHandler = ReadTableHandler(db_handler)
        self.beReadTableHandler = BeReadTableHandler(db_handler)
        self.popularRankTableHandler = PopularRankTableHandler(db_handler)
        self.redisHandler = RedisHandler()
        
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
        