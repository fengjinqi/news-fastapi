"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional

from sqlalchemy import String, Integer, Index, Enum
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import BaseModel


class User(BaseModel):
    """
    用户模型
    """
    __tablename__ = "users"
    __table_args__ = (
        # 添加索引
        Index('idx_username', 'username'),
        Index('idx_phone', 'phone'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg", comment="头像")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male','female','other'), comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(255), comment="简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment="手机")

    def __repr__(self):
        return f"<UserModel(id={self.id}, username={self.username}, avatar={self.avatar}, gender={self.gender}, bio={self.bio}, phone={self.phone})>"