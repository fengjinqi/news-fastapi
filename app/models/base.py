"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.core.db import Base
from sqlalchemy import Column, Integer, DateTime, func



class BaseModel(Base):
    """
    BaseModel
    """
    __abstract__ = True  # 声明此类为抽象基类，不会在数据库中创建对应的表，仅用于被其他模型继承
    id = Column(Integer, primary_key=True, autoincrement=True,comment="主键ID")
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now(), insert_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime] = mapped_column(DateTime,server_onupdate=func.now(), onupdate=func.now(),server_default=func.now(), default=func.now(), comment="更新时间")