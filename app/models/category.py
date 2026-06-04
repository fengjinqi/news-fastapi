"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""

from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class CategoryModel(BaseModel):
    """
    类别模型
    """
    __tablename__ = "new_category"
    id:  Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(100), unique=True,comment="类别名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

