"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.favorite_crud import FavoriteCrud
from app.models.users import User


async def get_favorite(db:AsyncSession, current_user:User, id:int)->bool:
    return await FavoriteCrud.get_favorite(db, current_user, id)


def create_favorite(param, db, current_user):
    return None