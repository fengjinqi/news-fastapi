"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ResponseModel, resp_success, resp_error
from app.schems.category import CategoryOut, CategoryIn
from app.services.category_service import CategoryService

router = APIRouter(prefix="/category", tags=["分类"])


@router.get("")
async def get_news_category(db: AsyncSession = Depends(get_db)) -> ResponseModel:
    data = await CategoryService.read(db)
    return resp_success(data=[CategoryOut.model_validate(item).model_dump() for item in data])


@router.post("")
async def create_news_category(param: CategoryIn, db: AsyncSession = Depends(get_db)) -> ResponseModel:
    obj = await CategoryService.create(db, param)
    return resp_success(data=CategoryOut.model_validate(obj).model_dump())


@router.put("/{id}")
async def update_news_category(id: int, param: CategoryIn, db: AsyncSession = Depends(get_db)) -> ResponseModel:
    obj = await CategoryService.update(db, id, param)
    if obj is None:
        return resp_error(code=404, message="分类不存在")
    return resp_success(data=CategoryOut.model_validate(obj).model_dump())


@router.delete("/{id}")
async def delete_news_category(id: Annotated[int, Path(gt=1, title='"分类ID"')],
                               db: AsyncSession = Depends(get_db)) -> ResponseModel:
    obj =await CategoryService.delete(db, id)

    if obj is None:
        return resp_error(code=404, message="分类不存在")
    return resp_success()
