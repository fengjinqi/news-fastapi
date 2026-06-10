"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Index, UniqueConstraint, ForeignKey

from app.models.base import BaseModel
class FavoriteModel(BaseModel):
    __tablename__ = "favorite"
    __table_args__ = (
        # 添加索引
        UniqueConstraint('user_id', 'news_id'),
        Index('idx_user_id', 'user_id'),
        Index('idx_news_id', 'news_id'),
    )
    id:Mapped[int]=mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.id"), nullable=False, comment="新闻ID")

    def __repr__(self):
        return f"<FavoriteModel(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"