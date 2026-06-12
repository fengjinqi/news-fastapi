"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:27 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from fastapi import APIRouter

from app.api import news, category, users, favorite, history

router = APIRouter()
router.include_router(news.router)
router.include_router(category.router)
router.include_router(users.router)
router.include_router(favorite.router)
router.include_router(history.router)
