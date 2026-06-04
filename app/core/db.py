"""
@Author    : fengjinqi
@Time      : 2026/6/4 12:48 PM
@Email     : fengjinqi1204@gmail.com
@File      : db.py
@Software  : PyCharm
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config.setting import settings

Base = declarative_base()

# 创建异步数据库引擎
async_engine = create_async_engine(
    settings.DATABASE_URL,  # 数据库连接URL，格式如：postgresql+asyncpg://user:password@host/dbname
    echo=True,  # 是否打印SQL日志，生产环境建议设为False
    future=True,  # 使用 SQLAlchemy 2.0 API 风格
    echo_pool=True,  # 连接池日志，调试时开启
    pool_size=10,  # 连接池常驻连接数（根据并发量调整，一般5-20）
    max_overflow=20,  # 超出pool_size后允许临时创建的最大连接数
    pool_timeout=30,  # 获取连接的超时时间（秒），超时抛异常
    pool_recycle=3600,  # 连接最大存活时间（秒），防止MySQL默认8小时断开
    pool_pre_ping=True,  # 取连接前先探测存活，避免使用已断开的连接
    pool_reset_on_return="rollback",  # 连接归还池时的重置策略，rollback比commit更安全

)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定的异步数据库引擎
    class_=AsyncSession,  # 使用异步Session类
    autocommit=False,  # 禁用自动提交，需手动调用commit()
    autoflush=False,  # 禁用自动刷新，避免不必要的SQL执行
    expire_on_commit=False  # 提交后不过期对象属性，避免再次访问触发额外查询
)


async def get_db() -> AsyncSession:
    """
    获取数据库会话依赖项

    创建一个异步数据库会话，并在请求结束后自动处理提交、回滚和关闭操作。
    通常用于 FastAPI 的 Depends 依赖注入。

    Yields:
        AsyncSession: 异步数据库会话对象

    Raises:
        Exception: 如果数据库操作失败，将回滚事务并重新抛出异常
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def create_db():
    """
    创建数据库表结构
    根据 Base 中注册的模型元数据，在数据库中创建所有对应的表。
    如果表已存在，则不会重复创建。
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
