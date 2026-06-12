"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.deps import get_current_user
from app.core.response import ResponseModel, resp_success, resp_error
from app.models.users import User
from app.schems.history import HistoryRequest
from app.schems.news import NewsListResponse, NewsRespone
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["历史记录"])

@router.get("")
async def get_history(db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user),page:Annotated[int,Query(...,description="页码")]=1,
                      page_size:Annotated[int,Query(...,description="页大小")]=10)->ResponseModel[NewsListResponse]:
    history,total = await HistoryService.get_history(db,current_user,page,page_size)
    news_list = []
    for news, history in history:
        item = NewsRespone.model_validate(news).model_dump()
        item["view_time"] = history.view_time
        news_list.append(item)
    return resp_success(data=NewsListResponse(list=news_list,total=total),message= "获取历史记录成功")

@router.post("")
async def create_history(param:Annotated[HistoryRequest,Body(...,description="历史记录参数")], db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user))->ResponseModel[bool]:
    history = await HistoryService.create( param,db,current_user)
    return resp_success(history, "创建历史记录成功")


@router.delete("/{id}")
async def delete_history(id:Annotated[int,Path(gt=0,description="历史记录ID")], db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user))->ResponseModel:
    result=await HistoryService.delete_history(db, current_user, id)
    if not result:
        return resp_error(code=400, message="删除历史记录失败")
    return resp_success(data=True, message="删除历史记录成功")




