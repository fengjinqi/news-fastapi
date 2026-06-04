"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""


from pydantic import BaseModel, Field


class CategoryIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: int = Field(..., ge=0)

class CategoryOut(BaseModel):
    id: int
    name: str
    sort_order: int
    class Config:
        from_attributes = True