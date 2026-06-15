"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Sequence, Optional

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import CategoryModel
from app.schems.category import CategoryRequest


class CRUDCategory:
    """
    CRUD操作类
    """

    @staticmethod
    async def create(db: AsyncSession, param: CategoryRequest) -> CategoryModel:
        """
        创建数据
        :param param:
        :param db:
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
    async def update(db: AsyncSession, id: int, param: CategoryRequest) -> Optional[CategoryModel]:
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

        # 名称唯一性校验：仅当名称发生变化时检查
        if param.name != obj.name:
            existing = await db.execute(
                select(CategoryModel).where(CategoryModel.name == param.name)
            )
            if existing.scalar_one_or_none() is not None:
                raise ValueError("分类名称已存在")
        for key, value in param.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.flush()
        #await db.refresh(obj)
        return obj

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> Optional[CategoryModel]:
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
