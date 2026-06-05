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
from app.schems.news import NewsRespone, NewsListResponse
from app.services import news_service

router = APIRouter(prefix="/news", tags=["新闻"])


@router.get("", response_model=ResponseModel, summary="获取新闻分类列表")
async def get_news_category(db: AsyncSession = Depends(get_db),
                            page : Annotated[int, Query(gt=0, description="页码")] = 1,
                            size : Annotated[int, Query( description="每页数量")]=10) -> ResponseModel:
    news,total = await news_service.read(db, page, size)
    return resp_success(data=NewsListResponse(total=total, list=[NewsRespone.model_validate(item).model_dump() for item in news]))
