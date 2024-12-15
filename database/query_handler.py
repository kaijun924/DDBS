from base_handler import MongoDBHandler
from handler import UserTableHandler, ArticleTableHandler, ReadTableHandler, BeReadTableHandler, PopularRankTableHandler

class QueryHandeler():
    def __init__(self, db_handler: MongoDBHandler):
        self.userTableHandler = UserTableHandler(db_handler)
        self.articleTableHandler = ArticleTableHandler(db_handler)
        self.readTableHandler = ReadTableHandler(db_handler)
        self.beReadTableHandler = BeReadTableHandler(db_handler)
        self.popularRankTableHandler = PopularRankTableHandler(db_handler)
        
    def fetch_users(self, conditions={}, count=100, offset=0):
        return self.userTableHandler.fetch_users(conditions, count, offset)
    
    def fetch_users_by_region(self, region: str, count=100, offset=0):
        return self.userTableHandler.fetch_users_by_region(region, count, offset)
    
    def fetch_articles(self, conditions={}, count=100, offset=0):
        return self.articleTableHandler.fetch_articles(conditions, count, offset)
    
    def fetch_articles_by_category(self, category: str, count=100, offset=0):
        return self.articleTableHandler.fetch_articles_by_category(category, count, offset)
    
    def fetch_reads(self, conditions={}, count=100, offset=0):
        return self.readTableHandler.fetch_reads(conditions, count, offset)
    
    def fetch_user_read(self, uid: str):
        user = self.userTableHandler.fetch_users({"uid": uid})
        reads = self.readTableHandler.fetch_reads_by_user(uid)   
        return {
            "user": user,
            "reads": reads
        }
        