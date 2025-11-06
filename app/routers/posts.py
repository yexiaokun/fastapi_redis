from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.models.post import PostCreate, PostInDB
from app.database import db
from bson import ObjectId
from typing import List



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[PostInDB], summary="获取所有文章")
async def get_posts():
    posts_cursor = db.posts.find({})
    posts = await posts_cursor.to_list(length=None)
    return [PostInDB(**post) for post in posts]

@router.get("/{post_id}")
def get_post(post_id: int):
    return {"message": f"获取文章 {post_id} 的内容"}

@router.get("/user/me",response_model=List[PostInDB], summary="获取当前用户的文章")
async def get_my_posts(current_user: dict = Depends(get_current_user)):
    posts_cursor = db.posts.find({"author_id": current_user["_id"]})
    posts = await posts_cursor.to_list(length=None)
    return [PostInDB(**post) for post in posts]


@router.post("/", response_model=PostInDB, summary="创建文章")
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    new_post = {
        "title": post.title,
        "content": post.content,
        "author_id": current_user["_id"]
    }

    result = await db.posts.insert_one(new_post)

    created_post = await db.posts.find_one({"_id": result.inserted_id})
    if not created_post:
        raise HTTPException(status_code=500, detail="文章创建失败")
    
    return PostInDB(**created_post)