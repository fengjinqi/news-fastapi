"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.category_crud import CRUDCategory
from app.models.category import CategoryModel
from app.schems.category import CategoryRequest


class CategoryService:
    """
    分类服务类
    """

    @staticmethod
    async def read(db: AsyncSession) -> Sequence[CategoryModel]:
        """
        查询分类
        :return: 查询的分类
        """
        return await CRUDCategory.read(db)

    @staticmethod
    async def create(db: AsyncSession, param: CategoryRequest) -> CategoryModel:
        """
        创建分类
        :param db:
        :param param: 分类参数
        :return: 创建的分类
        """

        return await CRUDCategory.create(db, param)

    @staticmethod
    async def update(db: AsyncSession, id: int, param: CategoryRequest) -> Optional[CategoryModel]:
        """
        更新分类
        :param db: 数据库会话
        :param id: 分类ID
        :param param: 分类参数
        :return: 更新的分类
        """
        return await CRUDCategory.update(db, id, param)

    @staticmethod
    async def delete(db: AsyncSession, id: int):
        return await CRUDCategory.delete(db, id)

