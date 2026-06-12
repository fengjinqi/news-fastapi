"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.category_crud import CRUDCategory
from app.models.category import CategoryModel
from app.schems.category import CategoryRequest, CategoryResponse
from app.utils.RedisUtil import RedisUtil


class CategoryService:
    """
    分类服务类
    """
    _cache_key = "category:all"

    @staticmethod
    async def read(db: AsyncSession) -> list[CategoryResponse]:
        """
        查询分类
        :return: 查询的分类
        """

        cached = await RedisUtil.get(CategoryService._cache_key)
        if cached:
            return cached
        _list= await CRUDCategory.read(db)
        result=[CategoryResponse.model_validate(item).model_dump(mode="json") for item in _list]
        await RedisUtil.set(CategoryService._cache_key, result,None)
        return result

    @staticmethod
    async def create(db: AsyncSession, param: CategoryRequest) -> CategoryModel:
        """
        创建分类
        :param db:
        :param param: 分类参数
        :return: 创建的分类
        """
        obj = await CRUDCategory.create(db, param)
        await RedisUtil.delete(CategoryService._cache_key)
        return obj

    @staticmethod
    async def update(db: AsyncSession, id: int, param: CategoryRequest) -> Optional[CategoryModel]:
        """
        更新分类
        :param db: 数据库会话
        :param id: 分类ID
        :param param: 分类参数
        :return: 更新的分类
        """
        obj=await CRUDCategory.update(db, id, param)
        await RedisUtil.delete(CategoryService._cache_key)
        return obj

    @staticmethod
    async def delete(db: AsyncSession, id: int):
        obj=await CRUDCategory.delete(db, id)
        await RedisUtil.delete(CategoryService._cache_key)
        return obj

