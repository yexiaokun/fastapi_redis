from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from app.database import db
from app.auth import create_access_token
from app.models.user import UserCreate, UserLoginRequest, UserResponse, UserTokenResponse
import bcrypt


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

@router.post("/register",response_model=UserResponse)
async def register_user(user: UserCreate):
    
    #查询用户名或邮箱是否存在
    existing_user = await db["users"].find_one({
        "$or": [{"username": user.username},{"email": user.email}]
    })
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    
    # 加密密码
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw.decode('utf-8')
    }

    await db["users"].insert_one(new_user)

    return UserResponse(username=user.username, email=user.email)

@router.post("/login",response_model=UserTokenResponse)
async def login_user(login: UserLoginRequest):
    #查找用户
    user = await db["users"].find_one({"username": login.username})
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    #效验密码
    if not bcrypt.checkpw(login.password.encode("utf-8"), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    #生成token
    access_token = create_access_token(data={"sub": login.username})

    return {"access_token": access_token, "token_type": "bearer"}