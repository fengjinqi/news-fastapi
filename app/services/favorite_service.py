"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Tuple

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.favorite_crud import FavoriteCrud
from app.models.news import NewsModel
from app.models.users import User
from app.schems.favorite import FavoriteRequest


async def get_favorite(db:AsyncSession, current_user:User, id:int)->bool:
    return await FavoriteCrud.get_favorite(db, current_user, id)


async def create_favorite(param:FavoriteRequest, db:AsyncSession, current_user:User)->bool:
    return await FavoriteCrud.create(param, db, current_user)


async def get_favorite_list(db:AsyncSession, current_user:User, page:int, size:int)-> Tuple[Sequence[Row[tuple[NewsModel, str]]], int | None]:
    return await FavoriteCrud.get_favorite_list(db, current_user, page, size)


async def delete_favorite(db:AsyncSession, current_user:User, id:int)->bool:
    return await FavoriteCrud.delete_favorite(db, current_user, id)
