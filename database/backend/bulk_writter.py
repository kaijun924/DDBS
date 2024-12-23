from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler
from query_handler import UnifiedHandler, QueryHandeler  # Assuming the classes are in query_handler.py


if __name__ == "__main__":
    # Initialize UnifiedHandler and QueryHandler
    unified_handler = UnifiedHandler()
    query_handler = QueryHandeler(unified_handler)
    
    
    # db_folder = "/Users/ckh/TsingHua清华/Phd/Sem1/DistributedDatabaseSystems/Assignment/project/code/db-generation/"
    query_handler.bulk_insert()

