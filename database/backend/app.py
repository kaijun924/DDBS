from fastapi import FastAPI, HTTPException, Query
from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler
from query_handler import UnifiedHandler, QueryHandeler  # Assuming the classes are in query_handler.py

# Initialize FastAPI
app = FastAPI()

# Initialize UnifiedHandler and QueryHandler
unified_handler = UnifiedHandler()
query_handler = QueryHandeler(unified_handler)


@app.get("/users/{uid}")
async def get_user_by_id(uid: str):
    """
    Fetch user by ID.
    """
    try:
        user = query_handler.fetch_user_by_id(uid)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles/{aid}")
async def get_article_by_id(aid: str):
    """
    Fetch article by ID.
    """
    try:
        article = query_handler.fetch_article_by_id(aid)
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/articles/category")
async def get_articles_by_category(
    category: str = Query("science", description="The category 'science' or 'technology'"), 
    count: int = Query(100, ge=1, le=1000, description="Number of articles to fetch"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Fetch articles by category with pagination.
    """

    try:
        articles = query_handler.fetch_articles_by_category(category, count, offset)
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reads/{bid}")
async def get_read_by_id(bid: str):
    """
    Fetch read information by ID.
    """
    try:
        read = query_handler.fetch_reads_by_id(bid)
        return read
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hadoop/article/{id}")
async def get_article_content_by_id(id: int):
    """
    Fetch article content by ID from Hadoop.
    """
    try:
        content = query_handler.fetch_article_content_by_id(id)
        return content
    except Exception as e:   
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/popular-rank/{id}")
async def get_popular_rank_by_id(id: int):
    """
    Fetch popular rank by ID.
    """
    try:
        rank = query_handler.fetch_popularRank_by_id(id)
        return rank
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))