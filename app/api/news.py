"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:48 AM
@Email     : fengjinqi1204@gmail.com
@File      : news.py
@Software  : PyCharm
"""
from fastapi import APIRouter
router = APIRouter(prefix="/news",tags=["news"])

@router.get("/category")
async def get_news_category():
    return {"message": "Hello World"}


@router.get("/")
async def get_news():
    return {"message": "Hello World"}