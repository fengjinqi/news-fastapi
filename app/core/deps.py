"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.users import User
from app.core.jwt import decode_access_token
from app.services import users_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login/form")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效或过期的token")
    user_id = int(payload.get("sub"))
    user = await users_service.read(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user