"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.user_crud import CRUDUser
from app.models.users import User
from app.schems.user import UserRegisterRequest, UserRequest, UserPasswordRequest
from app.utils.security import verify_password

if __name__ == '__main__':
    from pwdlib import PasswordHash

    pwd_hash = PasswordHash.recommended()

    # 加密
    hashed = pwd_hash.hash("12345678")
    print(
        hashed)
    # 验证
    print(pwd_hash.verify("12345678", hashed))  # # True


async def create(db: AsyncSession, user: UserRegisterRequest) -> User:
    return await CRUDUser.create(db, user)


async def login(db: AsyncSession, username: str, password: str) -> Optional[User]:
    user = await CRUDUser.get_by_username(db, username)
    if user is None or not verify_password(password, user.password):
        return None
    return user



async def read(db: AsyncSession, user_id: int) -> Optional[User]:
    return await CRUDUser.read(db, user_id)


async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
    return await CRUDUser.get_by_username(db, username)


async def update(db: AsyncSession, id:int, param:UserRequest)->Optional[User]:
    return await CRUDUser.update(db, id, param)


async def update_password(db: AsyncSession, id:int, param:UserPasswordRequest)->Optional[User]:
    return await CRUDUser.update_password(db, id, param)