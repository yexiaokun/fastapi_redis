from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_posts():
    return {"message": "获取文章列表"}

@router.get("/{post_id}")
def get_post(post_id: int):
    return {"message": f"获取文章 {post_id} 的内容"}