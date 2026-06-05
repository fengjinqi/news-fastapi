"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from pydantic import BaseModel, field_serializer
from typing import Optional, List
from datetime import datetime


class NewsRespone(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    author: str
    content: str
    image: Optional[str] = None
    category_id: int
    views: int = 0
    publish_time: Optional[datetime] = None

    @field_serializer("publish_time")
    def serialize_publish_time(self, v: Optional[datetime]) -> Optional[str]:
        return v.strftime("%Y-%m-%d %H:%M:%S") if v else None

    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    total: int
    list: List[NewsRespone]