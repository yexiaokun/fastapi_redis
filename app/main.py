from fastapi import FastAPI
from app.routers import users, posts


app = FastAPI(title="FastAPI ~ Redis Blog")


app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def read_root():
    return {"message": "欢迎来到我的个人博客！"}