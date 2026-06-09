"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite import FavoriteModel
from app.models.users import User


class FavoriteCrud:
    """
    收藏操作类
    """

    @staticmethod
    async def create(db: AsyncSession, user_id: int, news_id: int) -> bool:
        """
        创建收藏
        :param db: 数据库会话
        :param user_id: 用户ID
        :param news_id: 新闻ID
        :return: 是否成功
        """
        pass

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
    async def get_favorite_list(db: AsyncSession, user_id: int, page: int, page_size: int) -> bool:
        """
        获取收藏列表
        :param db: 数据库会话
        :param user_id: 用户ID
        :param page: 页码
        :param page_size: 页大小
        :param page_size: 页大小
        :return: 是否成功
        """
        pass
