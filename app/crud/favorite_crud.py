"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Tuple

from sqlalchemy import select, Row, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import CategoryModel
from app.models.favorite import FavoriteModel
from app.models.news import NewsModel
from app.models.users import User
from app.schems.favorite import FavoriteRequest


class FavoriteCrud:
    """
    收藏操作类
    """

    @staticmethod
    async def create(param: FavoriteRequest, db: AsyncSession, current_user: User) -> bool:
        """
        创建收藏
        :param param: 参数
        :param db: 数据库会话
        :param current_user: 当前用户
        :return: 是否成功
        """
        news = await db.execute(select(NewsModel).where(NewsModel.id == param.news_id))
        if not news.scalars().first():
            raise ValueError("新闻不存在")
        favorite = await db.execute(select(FavoriteModel).where(FavoriteModel.user_id == current_user.id,
                                                                FavoriteModel.news_id == param.news_id))
        if favorite.scalar_one_or_none():
            raise ValueError("已收藏")
        obj = FavoriteModel(user_id=current_user.id, news_id=param.news_id)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj is not None

    @staticmethod
    async def delete(db: AsyncSession, user_id: int, news_id: int) -> bool:
        """
        删除收藏
        :param db: 数据库会话
        :param user_id: 用户ID
        :param news_id: 新闻ID
        :return: 是否成功
        """
        pass

    @staticmethod
    async def get_favorite(db: AsyncSession, user_id: User, news_id: int) -> bool:
        """
        获取收藏
        :param db: 数据库会话
        :param user_id: 用户ID
        :param news_id: 新闻ID
        :return: 是否成功
        """
        result = await db.execute(
            select(FavoriteModel).where(FavoriteModel.user_id == user_id.id, FavoriteModel.news_id == news_id))
        obj = result.scalar_one_or_none()
        return obj is not None

    @staticmethod
    async def get_favorite_list(db: AsyncSession, user_id: User, page: int, page_size: int) -> Tuple[
        Sequence[Row[tuple[NewsModel, str]]], int | None]:
        """
        获取收藏列表
        :param db: 数据库会话
        :param user_id: 用户ID
        :param page: 页码
        :param page_size: 页大小
        :param page_size: 页大小
        :return: 是否成功
        """
        result = await db.execute(
            select(NewsModel, CategoryModel.name.label('category_name'))
            .where(NewsModel.id.in_(select(FavoriteModel.news_id).where(FavoriteModel.user_id == user_id.id)))
            .join(CategoryModel, NewsModel.category_id == CategoryModel.id)
            .limit(page_size).offset((page - 1) * page_size))
        total = await db.scalar(select(func.count()).where(FavoriteModel.user_id == user_id.id))

        return result.all(), total
