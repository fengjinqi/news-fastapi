"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class UserRegisterRequest(BaseModel):
    username:str= Field(..., min_length=3, max_length=20, description="用户名")
    password: str= Field(..., min_length=8, max_length=20, description="密码")
    password_confirm: str= Field(..., min_length=8, max_length=20, description="确认密码")

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("两次密码不一致")
        return self

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    class Config:
        from_attributes = True