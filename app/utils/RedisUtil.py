"""
@Author    : fengjinqi
@Time      : 2026/6/15 11:37
@Email     : fengjinqi1204@gmail.com
@File      : RedisUtil.py
@Software  : IntelliJ IDEA
"""
import json
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any
from uuid import UUID

from redis.asyncio import Redis

from app.core.redis import get_redis_pool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RedisUtil:
    """
    Redis工具类
    """

    @staticmethod
    def __json_serializer(obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        raise TypeError(f"不支持的序列化类型: {type(obj)}")

    @staticmethod
    def _get_client() -> Redis:
        """内部统一获取全局Redis客户端"""
        try:
            return get_redis_pool()
        except RuntimeError as e:
            logger.error(f"Redis客户端未初始化: {e}")
            raise

    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """
        从缓存中获取数据
        :param key: 缓存键
        :return: 缓存数据
        """
        try:
            val = await RedisUtil._get_client().get(key)
            if val is None:
                return None
            return json.loads(val if isinstance(val, str) else val.decode("utf-8"))
        except Exception as e:
            logger.warning(f"cache_get 失败 key={key} error={e}")
            return None

    @staticmethod
    async def set(key: str, value: Any, ex: Optional[int] = 300) -> bool:
        """
        将数据保存到缓存中
        :param ex: 缓存有效期（秒）
        :param key: 缓存键
        :param value: 缓存数据
        :return: 是否成功
        """
        try:
            if hasattr(value, "model_dump_json"):
                val = value.model_dump_json()
            else:
                # value: 需要序列化的 Python 对象
                # ensure_ascii=False: 允许非 ASCII 字符（如中文）直接输出，不会被转义为 \uXXXX 形式
                val = json.dumps(value, ensure_ascii=False, default=RedisUtil.__json_serializer)
            if ex is None:
                await RedisUtil._get_client().set(key, val)
            else:
                await RedisUtil._get_client().set(key, val, ex=ex)
            return True
        except Exception as e:
            logger.warning(f"cache_set 失败 key={key} error={e}")
            return False

    @staticmethod
    async def delete(key: str) -> bool:
        """
        删除缓存数据
        :param key: 缓存键
        :return: 是否成功
        """
        try:
            await RedisUtil._get_client().delete(key)
            return True
        except Exception as e:
            logger.warning(f"cache_delete 失败 key={key} error={e}")
            return False

    @staticmethod
    async def exists(key: str) -> bool:
        """
        判断缓存是否存在
        :param key: 缓存键
        :return: 是否存在
        """
        try:
            return bool(await RedisUtil._get_client().exists(key))
        except Exception as e:
            logger.warning(f"cache_exists 失败 key={key} error={e}")
            return False

    @staticmethod
    async def incr(key: str, amount: int = 1, ex: int = None) -> int:
        """
        缓存自增
        :param key: 缓存键
        :param amount: 自增数量
        :param ex: 过期时间
        :return: 自增后的值
        """
        try:
            count = await RedisUtil._get_client().incr(key, amount)
            if count == amount and ex is not None:
                await RedisUtil._get_client().expire(key, ex)
            return count
        except Exception as e:
            logger.warning(f"cache_incr 失败 key={key} error={e}")
            return 0
