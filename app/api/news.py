"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:48 AM
@Email     : fengjinqi1204@gmail.com
@File      : news.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import resp_success, ResponseModel


router = APIRouter(prefix="/news", tags=["新闻"])


@router.get("", response_model=ResponseModel, summary="获取新闻分类列表")
async def get_news_category(db: AsyncSession = Depends(get_db), page = Annotated[int, Query(1, description="页码")], size = Annotated[int, Query(10, description="每页数量")]) -> ResponseModel:

    return resp_success()
