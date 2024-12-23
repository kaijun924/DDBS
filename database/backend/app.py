from fastapi import FastAPI, HTTPException, Query
from service_mongo.handler import MongoDBHandler
from service_redis.handler import RedisHandler
from service_hadoop.handler import HadoopHandler
from query_handler import UnifiedHandler, QueryHandeler  # Assuming the classes are in query_handler.py
from io import BytesIO
from PIL import Image
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import Response
from boost import videos
import os

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


@app.get("/hadoop/article_txt/{id}")
async def get_article_txt(id: int):
    """
    Fetch article content by ID from Hadoop.
    """
    try:
        contents = query_handler.fetch_article_content_by_id(id)
        for key in contents.keys():
            if key.endswith('.txt'):
                return contents[key].decode()
    except Exception as e:   
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hadoop/article_img_num/{id}")
async def get_article_img_num(id: int):
    try:
        contents = query_handler.fetch_article_content_by_id(id)
        num = 0
        for key in contents.keys():
            if key.endswith('.jpg'):
                num += 1
        return {"total_images": num}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hadoop/article_img/{id}_{nth}")
async def get_article_img(id: int, nth: int):
    """
    Fetch article content by ID from Hadoop.
    """
    try:
        contents = query_handler.fetch_article_content_by_id(id)
        num = 0
        for key in contents.keys():
            if key.endswith('.jpg'):
                new_val = key.replace('.jpg', '')
                _,_,val = new_val.split('_')
                if int(val) == nth:
                    return StreamingResponse(content=BytesIO(contents[key]), media_type="image/jpeg")            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hadoop/article_video_query")
async def get_article_video_list():
    """
    Fetch article content by ID from Hadoop.
    """
    try:
        return videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hadoop/article_video/{id}")
async def get_article_video(id: int):
    """
    Fetch article content by ID from Hadoop.
    """
    try:
        contents = query_handler.fetch_article_video(id)
        for key in videos:
            new_val = key.replace('.flv', '')
            _,val,_ = new_val.split('_')
            val = val.replace("a", "")
            if int(val) == id:
                def iterfile():
                    val = videos[key]
                    val = val.replace("./", "")
                    with open(f"../temp_result/{videos[key]}", "rb") as f:
                        yield from f
                video_name = videos[key]
                video_name = video_name.replace("./", "")
                file_name = f"../temp_result/{video_name}"
                file_size = os.path.getsize(file_name)
                file_like = open(file_name, mode="rb")
                headers = {
                    "Accept-Ranges": "bytes",
                    "Content-Length": f"{file_size}",
                    "Content-Type": "video/flv",
                    "Content-Disposition": f"attachment;file_name={video_name}"
                }
                return StreamingResponse(file_like, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hadoop/article_video_try/{id}")
async def main(id: int):
    contents = query_handler.fetch_article_video(id)
    video_path = "../temp_result"
    for key in videos:
        new_val = key.replace('.flv', '')
        _,val,_ = new_val.split('_')
        val = val.replace("a", "")
        if int(val) == id:
            video_name = videos[key]
            file_name = f"{video_path}/{video_name}"
            file_size = os.path.getsize(file_name)
            file_like = open(file_name, mode="rb")
            headers = {
                "Accept-Ranges": "bytes",
                "Content-Length": f"{file_size}",
                "Content-Type": "video/flv",
                "Content-Disposition": f"attachment;file_name={video_name}"
            }
            return StreamingResponse(file_like, headers=headers)

    



@app.post("/popular-rank/{temporalGranularity}")
async def get_popular_rank_by_id(temporalGranularity: str):
    """
    Fetch popular rank by ID.
    """
    try:
        rank = query_handler.fetch_popularRank_by_id({"temporalGranularity":temporalGranularity})
        # if rank["_id"]:
        #     del rank["_id"]
        # print(rank)
        return rank
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))