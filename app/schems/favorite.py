"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from pydantic import BaseModel, Field


class FavoriteRequest(BaseModel):
    """
    收藏参数
    """
    news_id: int = Field(..., description="新闻ID")
    class Config:
        from_attributes = True
