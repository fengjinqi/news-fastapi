"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from app.schems.news import NewsRespone
from app.utils.RedisUtil import RedisUtil

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import news_crud


async def read(db: AsyncSession, id: int, page: int, size: int) -> tuple[list[NewsRespone], int]:
    """
    查询新闻
    :param db:
    :param id:
    :param page:
    :param size:
    :return:
    """
    cache_key = f"news:category:{id}:page:{page}:size:{size}"
    cached = await RedisUtil.get(cache_key)
    if cached:
        return cached["list"], cached["total"]
    news, total = await news_crud.read(db, id, page, size)
    result = [NewsRespone.model_validate(item).model_dump(mode="json") for item in news]
    await RedisUtil.set(cache_key, {
        "list": result,
        "total": total
    }, None)
    return result, total


FLUSH_THRESHOLD = 10


async def read_detail(db: AsyncSession, id: int) -> NewsRespone:
    """
    查询新闻详情
    :param db:
    :param id:
    :return:
    """
    cache_key = f"news:detail:{id}"
    views_key = f"news:views:{id}"
    delta = await RedisUtil.incr(views_key)
    if delta >= FLUSH_THRESHOLD:
        await news_crud.increment_views(db, id, delta)
        await RedisUtil.delete(views_key)
        await RedisUtil.delete(cache_key)
        delta = 0
    cached = await RedisUtil.get(cache_key)
    if cached:
        cached['views'] = cached['views'] + delta
        return cached
    news, category_name, related_news = await news_crud.read_detail(db, id)
    newResult = NewsRespone.model_validate(news).model_dump(mode="json")
    newResult["category_name"] = category_name
    newResult["related_news"] = [NewsRespone.model_validate(item).model_dump(mode="json") for item in related_news]
    newResult["views"] = news.views + delta
    if news is not None:
        await RedisUtil.set(cache_key, newResult, None)
    return newResult
