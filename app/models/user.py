from pydantic import BaseModel, Field, EmailStr




class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=20, description="用户名长度需在1~20之间")
    password: str = Field(..., min_length=6, description="密码至少6位")
    email: EmailStr = Field(..., description="必须是有效邮箱格式")

class UserResponse(BaseModel):
    username: str
    email: EmailStr

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"