"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.models.category import CategoryModel
from app.models.news import NewsModel


async def read(db: AsyncSession, id: int, page: int, size: int) -> tuple[Sequence[NewsModel], int]:
    """
    查询新闻
    :param id:
    :param page:
    :param size:
    :param db: 数据库会话
    :return: 查询的新闻
    """
    # print( await db.scalar(count(NewsModel.id)))
    total = await db.scalar(select(func.count()).select_from(NewsModel).where(NewsModel.category_id == id))
    result = await db.execute(
        select(NewsModel).where(NewsModel.category_id == id).offset((page - 1) * size).limit(size))

    return result.scalars().all(), total


async def read_detail(db: AsyncSession, id: int) -> tuple[Optional[NewsModel], Optional[str], Sequence[NewsModel]]:
    """
    查询新闻详情
    并且更新新闻的浏览次数
    :param db: 数据库会话
    :param id: 新闻id
    :return: 新闻详情
    """

    result = await db.execute(
        select(NewsModel, CategoryModel.name.label("category_name")).where(NewsModel.id == id).join(CategoryModel,
                                                                                                    NewsModel.category_id == CategoryModel.id))
    row = result.first()
    if row is None:
        return None, None, []
    news, category_name = row[0], row[1]
    await db.execute(update(NewsModel).where(NewsModel.id == id).values(views=NewsModel.views + 1))
    # 查询同分类下的相关新闻（排除当前新闻），按浏览量和发布时间降序排列，取前5条
    related_news_result = await db.execute(
        select(NewsModel)
        .where(NewsModel.category_id == row[0].category_id, NewsModel.id != id)
        .order_by(NewsModel.views.desc(), NewsModel.publish_time.desc())
        .limit(5)
    )
    related_news = related_news_result.scalars().all()
    # 返回当前新闻详情和分类名称
    return news, category_name, related_news


async def increment_views(db: AsyncSession, id: int, count: int) -> int:
    """
    增加新闻浏览次数
    :param db: 数据库会话
    :param id: 新闻id
    :param count: 增加的次数
    :return: 新闻的总浏览次数
    """
    await db.execute(update(NewsModel).where(NewsModel.id == id).values(views=NewsModel.views + count))
    result = await db.scalar(select(NewsModel.views).where(NewsModel.id == id))
    return result


