"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.users import User
from app.schems.user import UserRegisterRequest, UserRequest, UserPasswordRequest
from app.utils.security import hash_password, verify_password


class CRUDUser:

    @staticmethod
    async def create(db: AsyncSession, user: UserRegisterRequest) -> User:
        password = hash_password(user.password)
        obj = User(username=user.username, password=password)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def read(db: AsyncSession, user_id: int) -> Optional[User]:
        return await db.get(User, user_id)

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, id: int, param: UserRequest)-> Optional[User]:
        obj: Optional[User] = await db.get(User, id)
        if obj is None:
            return None
        if param.username is not None and param.username != obj.username:
            existing = await CRUDUser.get_by_username(db, param.username)
            if existing is not None:
                raise ValueError("用户名已存在")# 用户名已存在
        for key, value in param.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.flush()
        return obj

    @staticmethod
    async def update_password(db: AsyncSession, id: int, param:UserPasswordRequest)-> Optional[User]:
        obj: Optional[User] = await db.get(User, id)
        if obj is None:
            raise ValueError("用户不存在")
        if not verify_password(param.old_password, obj.password):
            raise ValueError("旧密码错误")
        obj.password = hash_password(param.new_password)
        await db.commit()
        await db.refresh(obj)
        return obj
