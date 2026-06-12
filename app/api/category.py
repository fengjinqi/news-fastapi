"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ResponseModel, resp_success, resp_error

from app.schems.category import CategoryRequest, CategoryResponse
from app.services.category_service import CategoryService
from app.core.deps import get_current_user

router = APIRouter(prefix="/category", tags=["分类"])


@router.get("", summary="获取列表")
async def get_news_category(db: AsyncSession = Depends(get_db)) -> ResponseModel[list[CategoryResponse]]:
    data = await CategoryService.read(db)
    return resp_success(data=data)


@router.post("", dependencies=[Depends(get_current_user)], summary="创建分类")
async def create_news_category(param: CategoryRequest, db: AsyncSession = Depends(get_db)) -> ResponseModel[CategoryResponse]:
    obj = await CategoryService.create(db, param)
    return resp_success(data=CategoryResponse.model_validate(obj).model_dump())


@router.put("/{id}", dependencies=[Depends(get_current_user)], summary="更新分类")
async def update_news_category(id: Annotated[int, Path(gt=0, description="分类ID")],
                               param: Annotated[CategoryRequest, Body(..., description="分类参数")],
                               db: AsyncSession = Depends(get_db)) -> ResponseModel[CategoryResponse]:
    obj = await CategoryService.update(db, id, param)
    if obj is None:
        return resp_error(code=404, message="分类不存在")
    return resp_success(data=CategoryResponse.model_validate(obj).model_dump())


@router.delete("/{id}", dependencies=[Depends(get_current_user)], summary="删除分类")
async def delete_news_category(id: Annotated[int, Path(gt=1, description="分类ID")],
                               db: AsyncSession = Depends(get_db)) -> ResponseModel:
    obj = await CategoryService.delete(db, id)

    if obj is None:
        return resp_error(code=404, message="分类不存在")
    return resp_success()
