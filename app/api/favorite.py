"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ResponseModel, resp_success
from app.models.users import User
from app.schems.favorite import FavoriteRequest
from app.services import favorite_service
from app.core.deps import get_current_user

router = APIRouter(prefix="/favorite", tags=["收藏"])


@router.get("")
async def get_favorite(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                       id: Annotated[int, Query(gt=0, description="新闻ID")] = 0) -> ResponseModel:
    """
    获取收藏列表
    """
    result = await favorite_service.get_favorite(db, current_user, id)
    return resp_success(data=result, message="获取收藏状态成功")


@router.post("",  summary="收藏新闻")
async def create_favorite(     param: Annotated[FavoriteRequest, Body(..., description="收藏参数")],db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user),
                         ) -> ResponseModel:
    """
    收藏新闻
    """
    print(param.news_id,'=========')

    result = await favorite_service.create_favorite(param, db, current_user)
    return resp_success( message="收藏成功")


@router.delete("")
async def delete_favorite(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                          id: Annotated[int, Query(gt=0, description="新闻ID")] = 0) -> ResponseModel:
    """
    取消收藏
    """
    pass
    result = await favorite_service.delete_favorite(db, current_user, id)
    return resp_success(data=result, message="取消收藏成功")
