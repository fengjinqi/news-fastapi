"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Any, Coroutine, Sequence, Optional

from sqlalchemy import select, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import CategoryModel
from app.schems.category import CategoryOut, CategoryIn


class CRUDCategory:
    """
    CRUD操作类
    """

    @staticmethod
    async def create(db: AsyncSession, param: CategoryIn) -> CategoryModel:
        """
        创建数据
        :param kwargs: 数据
        :return: 创建的数据
        """
        obj = CategoryModel(**param.model_dump())
        db.add(obj)
        await db.flush()  # 执行 INSERT SQL
        await db.refresh(obj)
        return obj

    @staticmethod
    async def read(db: AsyncSession) -> Sequence[CategoryModel]:
        """
        查询数据
        :return: 查询数据
        """
        result = await db.execute(select(CategoryModel))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, id: int, param: CategoryIn) -> type[CategoryModel] | None:
        """
        更新数据
        :param db: 数据库会话
        :param id: 数据ID
        :param param: 更新数据
        :return: 更新后的数据
        """
        obj = await db.get(CategoryModel, id)
        if obj is None:
            return None

        for key, value in param.model_dump().items():
            setattr(obj, key, value)
        await db.flush()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> type[CategoryModel] | None:
        """
        删除数据
        :param db: 数据库会话
        :param id: 数据ID
        :return: 删除的数据
        """
        obj = await db.get(CategoryModel, id)
        if obj is None:
            return None
        await db.delete(obj)
        await db.flush()
        return obj
