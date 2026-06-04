"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Optional, Any

from pydantic import Field, BaseModel


class ResponseModel(BaseModel):
    """
    响应类
    """
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="状态信息")

    data: Optional[Any] = Field(default_factory=dict, description="数据")


def resp_success(data: Optional[Any] = None, message: str = "success") -> ResponseModel:
    """
    成功响应
    :param data: 数据
    :param message: 状态信息
    :return: 响应类
    """
    return ResponseModel(code=200, message=message, data=data)


def resp_error(code: int, message: str) -> ResponseModel:
    """
    错误响应
    :param code: 错误码
    :param message: 错误信息
    :return: 响应类
    """
    return ResponseModel(code=code, message=message)
