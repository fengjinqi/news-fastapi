"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.config.setting import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌

    :param data: 需要编码到令牌中的数据字典
    :param expires_delta: 令牌过期时间增量，若不传则使用配置中的默认过期时间
    :return: 编码后的 JWT 字符串
    """
    # 复制原始数据，避免修改传入的原始字典
    to_encode = data.copy()

    # 计算过期时间：若传入了 expires_delta 则使用，否则使用配置文件中的默认过期分钟数
    if expires_delta is not None:
        # 使用调用方指定的过期时间增量
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 使用配置中的默认过期时间（单位：分钟）
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 将过期时间写入 payload，JWT 标准字段 "exp" 表示令牌失效的时间戳
    to_encode.update({"exp": expire})

    # 使用配置中的密钥（SECRET_KEY）和加密算法（ALGORITHM）对 payload 进行编码，返回 JWT 字符串
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码 JWT 访问令牌

    :param token: 待解码的 JWT 字符串
    :return: 解码后的 payload 字典；若令牌已过期或无效则返回 None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # 令牌已过期
        return None
    except jwt.InvalidTokenError:
        # 令牌无效（签名错误、格式错误等）
        return None

def create_refresh_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)