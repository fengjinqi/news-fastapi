"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.models.news import NewsModel


async def read(db: AsyncSession, id: int, page: int, size: int) -> Tuple[Sequence[NewsModel],int]:
    """
    查询新闻
    :param id:
    :param page:
    :param size:
    :param db: 数据库会话
    :return: 查询的新闻
    """
    #print( await db.scalar(count(NewsModel.id)))
    total = await db.scalar(select(func.count()).select_from(NewsModel).where(NewsModel.category_id == id))
    result = await db.execute(select(NewsModel).where(NewsModel.category_id == id).offset((page - 1) * size).limit(size))

    return result.scalars().all(),total

