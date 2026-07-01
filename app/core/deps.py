"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Coroutine, Any, Callable

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import State

from app.core.db import get_db
from app.core.exceptions import AppBizException
from app.models.users import User
from app.core.jwt import decode_access_token
from app.services import users_service
from app.utils.RedisUtil import RedisUtil

from app.utils.logger import get_logger

logger = get_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login/form")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效或过期的token")
    user_id = int(payload.get("sub"))
    user = await users_service.read(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


def rate_limit(max_requests: int = 10, window_seconds: int = 60)-> Callable[
    [Request[State]], Coroutine[Any, Any, None]]:
    """
    限流器
    :param max_requests: 每个IP每分钟最多访问次数
    :param window_seconds: 时间窗口
    :return:
    """
    async def _rate_limiter(request: Request):
        client_ip = request.client.host if request.client else 'unknown'
        path = request.url.path
        rate_key = f"rate_limit:{client_ip}:{path}"
        try:
            count = await RedisUtil.incr(rate_key, ex=window_seconds)
            if count > max_requests:
                logger.warning(f"限流触发: {client_ip}:{path}")
                raise AppBizException(code=429, msg="请求过于频繁")
        except AppBizException:
            raise
        except Exception as e:
            logger.warning(f"限流降级放行: {client_ip}:{path} error={e}")
    return _rate_limiter
