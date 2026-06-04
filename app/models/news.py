"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from email.policy import default
from enum import unique

from sqlalchemy import Integer
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.models.base import BaseModel



class NewsModel(BaseModel):
    """
    新闻模型
    """
    # __tablename__ = "news"
    # id: int = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    # title: str = Column(String(255), comment="标题")
    # description: str = Column(String(255), comment="描述")
    # author: str = Column(String(255), comment="作者")
    # content: str = Column(Text, comment="内容")
