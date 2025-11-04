from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users():
    return {"message": "获取用户列表"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"获取用户 {user_id} 的信息"}