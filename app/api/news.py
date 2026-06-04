"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:48 AM
@Email     : fengjinqi1204@gmail.com
@File      : news.py
@Software  : PyCharm
"""
from typing import Annotated, Any, Coroutine

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.response import resp_success, ResponseModel
from app.schems.category import CategoryOut
from app.services.category_service import CategoryService

router = APIRouter(prefix="/news", tags=["news"])


