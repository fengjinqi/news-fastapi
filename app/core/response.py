"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional, TypeVar, Generic

from pydantic import Field, BaseModel

T = TypeVar("T")
class ResponseModel(BaseModel, Generic[T]):
    """
    响应类
    """
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="状态信息")

    data: Optional[T] = Field(default_factory=dict, description="数据")



def resp_success(data: Optional[T] = None, message: str = "success") -> ResponseModel[T]:
    """
    成功响应
    :param data: 数据
    :param message: 状态信息
    :return: 响应类
    """
    return ResponseModel(code=200, message=message, data=data)


def resp_error(code: int, message: str) -> ResponseModel[T]:
    """
    错误响应
    :param code: 错误码
    :param message: 错误信息
    :return: 响应类
    """
    return ResponseModel(code=code, message=message)
