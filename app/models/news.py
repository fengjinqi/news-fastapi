"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import  ForeignKey, DateTime, Index, Integer, String, Text

from sqlalchemy.orm import Mapped,mapped_column


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
    description: Mapped[Optional[str]] = mapped_column(String(255), comment="描述")
    author: Mapped[str] = mapped_column(String(255), nullable=False, comment="作者")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="图片")
#     CASCADE - 父记录删除，子记录同步删除
#     SET NULL - 父记录删除，子记录该字段置为 NULL
#     RESTRICT - 有子记录时禁止删除父记录（默认行为）
#     SET DEFAULT - 父记录删除，子记录该字段置为默认值
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("new_category.id"), nullable=False,comment="类别ID")
    views: Mapped[int] = mapped_column(Integer, default=0, comment="浏览次数")
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment="发布时间")

    def __repr__(self):
        return f"<NewsModel(id={self.id}, title={self.title}, content={self.content}, image={self.image}, category_id={self.category_id}, views={self.views}, publish_time={self.publish_time})>"