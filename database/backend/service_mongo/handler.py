from pymongo import MongoClient, errors

class MongoDBHandler:
    """Handles MongoDB operations."""

    def __init__(self, host: str, port: int):
        """Initialize the MongoDB connection."""
        self.redis_handler = None
        try:
            self.client = MongoClient(host, port)
            print(f"Connected to MongoDB at {host}:{port}")
            
            self.user_collection = self.client["userDatabase"]["User"]
            self.article_collection = self.client["articleDatabase"]["Article"]
            self.read_collection = self.client["readDatabase"]["Read"]
            self.be_read_collection = self.client["beReadDatabase"]["BeRead"]
            self.popular_rank_collection = self.client["popularRankDatabase"]["PopularRank"]
            
        except errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def get_database(self, db_name: str):
        """Retrieve a database."""
        return self.client[db_name]
    
    def set_redis_handler(self, redis_handler):
        self.redis_handler = redis_handler