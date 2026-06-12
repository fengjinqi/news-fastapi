"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.history_crud import HistoryCrud
from app.models.history import HistoryModel
from app.models.news import NewsModel
from app.models.users import User
from app.schems.history import HistoryRequest


class HistoryService:
    """
    历史记录服务类
    """
    @staticmethod
    async def create( param: HistoryRequest,db: AsyncSession
                     , current_user: User) -> bool:
        """
        创建历史记录
        :param current_user:
        :param db:
        :param param:
        :return:
        """
        return await HistoryCrud.create(param,db,current_user)

    @staticmethod
    async def get_history(db: AsyncSession, current_user: User, page: int, page_size: int) -> tuple[
        Sequence[Row[tuple[NewsModel, HistoryModel]]], int | None]:
        return await HistoryCrud.get_history(db, current_user, page, page_size)

    @staticmethod
    async def delete_history(db: AsyncSession, current_user: User, id: int)->bool:
        return await HistoryCrud.delete_history(db, current_user, id)




