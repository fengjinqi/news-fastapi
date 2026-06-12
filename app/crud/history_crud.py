"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from datetime import datetime
from typing import  Sequence

from sqlalchemy import select, func, Row, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.history import HistoryModel
from app.models.news import NewsModel
from app.models.users import User
from app.schems.history import HistoryRequest


class HistoryCrud:
    """
    历史记录CRUD
    """

    @staticmethod
    async def create(param: HistoryRequest, db: AsyncSession, current_user: User) -> bool:
        """
        创建历史记录
        :param current_user:
        :param db:
        :param param:
        :return:
        """
        news = await db.execute(select(NewsModel).where(NewsModel.id == param.news_id))
        if not news.scalar():
            raise ValueError("新闻不存在")

        result = await db.execute(
            select(HistoryModel).where(HistoryModel.user_id == current_user.id, HistoryModel.news_id == param.news_id))
        existing = result.scalar_one_or_none()
        if existing:
            existing.view_time = datetime.now()
            await db.flush()
            return True
        db.add(HistoryModel(user_id=current_user.id, news_id=param.news_id))
        await db.flush()
        return True

    @staticmethod
    async def get_history(db: AsyncSession, current_user: User, page: int, page_size: int)-> tuple[
        Sequence[Row[tuple[NewsModel, HistoryModel]]], int | None]:

        result = await db.execute(select(NewsModel,HistoryModel).where(HistoryModel.user_id == current_user.id).join(NewsModel, HistoryModel.news_id == NewsModel.id).order_by(HistoryModel.view_time.desc()).offset((page - 1) * page_size).limit(page_size))
        total = await db.scalar(select(func.count(HistoryModel.id)).where(HistoryModel.user_id == current_user.id))
        return result.all(), total

    @staticmethod
    async def delete_history(db: AsyncSession, current_user: User, id: int)->bool:
        """
        删除历史记录
        :param db:
        :param current_user:
        :param id:
        :return:
        """

        result =  await db.execute(delete(HistoryModel).where(HistoryModel.user_id == current_user.id, HistoryModel.news_id == id))

        return result.rowcount > 0 # type: ignore[call-arg]
