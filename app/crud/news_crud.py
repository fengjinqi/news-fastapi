"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Tuple

from sqlalchemy import select,  update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.models.category import CategoryModel
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


async def read_detail(db: AsyncSession, id:int)->Tuple[NewsModel, str]:
    """
    查询新闻详情
    并且更新新闻的浏览次数
    :param db: 数据库会话
    :param id: 新闻id
    :return: 新闻详情
    """
    result = await db.execute(select(NewsModel, CategoryModel.name.label("category_name")).where(NewsModel.id == id).join(CategoryModel, NewsModel.category_id == CategoryModel.id))
    row = result.first()
    if row:
        await db.execute(update(NewsModel).where(NewsModel.id == id).values(views=NewsModel.views + 1))

    return row[0],row[1]