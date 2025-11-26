from fastapi import FastAPI
from app.routers import users, posts
from app.database import db, redis_client


app = FastAPI(title="FastAPI ~ Redis Blog")


app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"message": "欢迎来到我的个人博客！"}

@app.get("/healthcheck")
async def healthcheck():
    try:
        collections = await db.list_collection_names()

        pong = await redis_client.ping()
        return {
            "status": "ok",
            "mongo_collections": collections,
            "redis_connected": pong
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}