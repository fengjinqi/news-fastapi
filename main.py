from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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
# 配置跨域资源共享（CORS）中间件
# 允许所有来源、方法和请求头访问 API，同时支持携带凭证（如 Cookie）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有来源域访问
    allow_credentials=True,       # 允许携带身份凭证（如 Cookie、Authorization 等）
    allow_methods=["*"],          # 允许所有 HTTP 方法（GET、POST、PUT、DELETE 等）
    allow_headers=["*"],          # 允许所有请求头
)

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
