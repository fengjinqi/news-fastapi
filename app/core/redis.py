"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from redis.asyncio import Redis, ConnectionPool
from typing import Optional, AsyncGenerator
from app.config.setting import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
_redis_client: Optional[Redis] = None


async def init_redis()-> None:
    """
    初始化Redis客户端
    """
    global _redis_client
    pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        max_connections=20,
        socket_connect_timeout=5,
        socket_timeout=5,
        health_check_interval=20
    )
    _redis_client = Redis(connection_pool=pool)
    try:
        await _redis_client.ping()
        logger.info(f"Redis 连接成功：{settings.REDIS_HOST}:{settings.REDIS_PORT} db={settings.REDIS_DB}")
    except Exception as e:
        logger.error(f"Redis 连接失败：{settings.REDIS_HOST}:{settings.REDIS_PORT} db={settings.REDIS_DB}，错误信息：{e}")





async def close_redis() -> None:
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None
        logger.info("Redis 连接已关闭")


def get_redis_pool() -> Redis:
    if _redis_client is None:
        raise RuntimeError("Redis 未初始化，请先在 lifespan 中调用 init_redis()")
    return _redis_client


async def get_redis() -> AsyncGenerator[Redis, None]:
    yield get_redis_pool()