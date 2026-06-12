"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import ResponseModel, resp_success, resp_error
from app.models.users import User
from app.schems.favorite import FavoriteRequest
from app.schems.news import NewsListResponse, NewsRespone
from app.services import favorite_service
from app.core.deps import get_current_user

router = APIRouter(prefix="/favorite", tags=["收藏"])


@router.get("/{id}", summary="根据新闻id获取收藏状态")
async def get_favorite(id:Annotated[int, Path(gt=0, description="新闻ID")],current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                       ) -> ResponseModel[bool]:
    """
    获取收藏列表
    """
    result = await favorite_service.get_favorite(db, current_user, id)
    return resp_success(data=result, message="获取收藏状态成功")

@router.get("", summary="获取我的收藏列表")
async def get_favorite_list(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                            page: Annotated[int, Query(gt=0, description="页码")] = 1,
                            size: Annotated[int, Query(gt=0, description="页大小")] = 10) -> ResponseModel[
    NewsListResponse]:
    """
    获取收藏列表
    """
    result,total = await favorite_service.get_favorite_list(db, current_user, page, size)
    news_list = []
    for item,name in result:
        news = NewsRespone.model_validate(item).model_dump()
        news["category_name"] = name
        news_list.append(news)


    return resp_success(data=NewsListResponse(total=total, list=news_list), message="获取收藏列表成功")


@router.post("",  summary="收藏新闻")
async def create_favorite(     param: Annotated[FavoriteRequest, Body(..., description="收藏参数")],db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user),
                         ) -> ResponseModel:
    """
    收藏新闻
    """
    result = await favorite_service.create_favorite(param, db, current_user)
    if not result:
        return resp_error(code=400, message="收藏失败")
    return resp_success( message="收藏成功")


@router.delete("/{id}")
async def delete_favorite(id: Annotated[int, Path(gt=0, description="新闻ID")],current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
                          ) -> ResponseModel:
    """
    取消收藏
    """
    result = await favorite_service.delete_favorite(db, current_user, id)
    if not result:
        return resp_error(code=400, message="取消收藏失败")
    return resp_success(data=result, message="取消收藏成功")
