from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler
from query_handler import UnifiedHandler, QueryHandeler  # Assuming the classes are in query_handler.py
from PIL import Image
from io import BytesIO


if __name__ == "__main__":
    # Initialize UnifiedHandler and QueryHandler
    unified_handler = UnifiedHandler()
    query_handler = QueryHandeler(unified_handler)
    
    
    db_folder = "/Users/ckh/TsingHua清华/Phd/Sem1/DistributedDatabaseSystems/Assignment/project/code/db-generation/"
    query_handler.bulk_insert(db_folder)
    
    # contents = query_handler.fetch_article_content_by_id(1010)
    # print(contents.keys())
    # for key in contents.keys():
    #     if key.endswith('.jpg'):
    #         img = Image.open(BytesIO(contents[key]))
    #         img.save(f'./{key}')
    #         print(f'Image {key} saved')
    #     elif key.endswith('.txt'):
    #         print(contents[key].decode())
    #     else:
    #         print(contents[key])

