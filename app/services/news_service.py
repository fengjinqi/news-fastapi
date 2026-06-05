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

from app.crud import news_crud
from app.models.news import NewsModel


async def read(db: AsyncSession, id: int, page: int, size: int) -> Tuple[Sequence[NewsModel],int]:
    return await news_crud.read(db,id, page, size)


async def read_detail(db: AsyncSession, id: int)-> Sequence[Row[tuple[NewsModel, str]]]:
    return await news_crud.read_detail(db, id)
