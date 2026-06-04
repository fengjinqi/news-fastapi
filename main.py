from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.core.db import create_db
from app.core.exceptions import register_exception


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await create_db()
    yield
    # shutdown（如有关闭逻辑写在这里）


app = FastAPI(lifespan=lifespan)
register_exception(app)
app.include_router(router=router, prefix="/api")

# @app.on_event("startup")
# async def startup_event():
#     """
#     应用启动事件处理函数。
#
#     在 FastAPI 应用启动时自动触发，执行初始化操作。
#     当前主要完成以下工作：
#         - 调用 create_db() 初始化数据库，确保数据表结构已创建。
#     """
#     await create_db()
