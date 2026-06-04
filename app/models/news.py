"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""

from datetime import datetime


from sqlalchemy import  ForeignKey, DateTime, Index, Integer, String, Text

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.models.base import BaseModel


class NewsModel(BaseModel):
    """
    新闻模型
    """
    __tablename__ = "news"
    __table_args__ = (
        # 添加索引
        Index('idx_category_id', 'category_id'),
        Index('idx_publish_time', 'publish_time'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="标题")
    description: Mapped[str] = mapped_column(String(255), comment="描述")
    author: Mapped[str] = mapped_column(String(255), nullable=False, comment="作者")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    image: Mapped[str] = mapped_column(String(255), comment="图片")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("new_category.id"), nullable=False,comment="类别ID")
    views: Mapped[int] = mapped_column(Integer, default=0, comment="浏览次数")
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment="发布时间")
