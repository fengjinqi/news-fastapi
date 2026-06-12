"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from sqlalchemy import Integer, ForeignKey,  func, Index, UniqueConstraint, column, TIMESTAMP


class HistoryModel(BaseModel):
    """
    历史记录
    """
    __tablename__ = "history"

    __table_args__ = (
        # 添加索引
        UniqueConstraint('user_id', 'news_id', name='uix_user_id_news_id'),
        Index('idx_user_id', 'user_id'),
        Index('idx_news_id', 'news_id'),
        Index('idx_view_time', column('view_time').desc())
    )

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,comment="主键ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.id",ondelete="CASCADE"), nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(TIMESTAMP,server_default=func.now(), default=func.now(), comment="查看时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"