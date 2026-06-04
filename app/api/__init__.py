"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:27 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from fastapi import APIRouter

from app.api import news

router = APIRouter()
router.include_router(news.router)
