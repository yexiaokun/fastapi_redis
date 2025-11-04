from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from app.database import db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=20, description="用户名长度需在1~20之间")
    password: str = Field(..., min_length=6, description="密码至少6位")
    email: EmailStr = Field(..., description="必须是有效邮箱格式")

class UserResponse(BaseModel):
    username: str
    email: EmailStr



@router.get("/")
def get_users():
    return {"message": "获取用户列表"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"获取用户 {user_id} 的信息"}

@router.post("/register",response_model=UserResponse)
async def register_user(user: UserCreate):
    
    #查询用户名或邮箱是否已存在
    existing_user = await db["users"].find_one({
        "$or": [{"username": user.username},{"email": user.email}]
    })
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    
    new_user = user.model_dump()
    result = await db["users"].insert_one(new_user)

    return user