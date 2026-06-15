import time
import uuid
from contextlib import asynccontextmanager


from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.api import router
from app.core.db import create_db
from app.core.exceptions import register_exception
from app.core.redis import init_redis, close_redis
from app.utils.logger import setup_logger, _trace_id_var, access_logger, get_logger
from fastapi import Request
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    setup_logger()  # uvicorn 启动后重新初始化，防止被覆盖
    try:
        await create_db()
    except Exception as e:
        logger.error(f"数据库初始化失败，请检查 MySQL 是否可达: {e}", exc_info=True)
        raise
    try:
        await init_redis()
    except Exception as e:
        logger.error(f"Redis 初始化失败: {e}", exc_info=True)
        raise
    yield
    await close_redis()
    # shutdown（如有关闭逻辑写在这里）


app = FastAPI(lifespan=lifespan)
# 配置跨域资源共享（CORS）中间件
# 允许所有来源、方法和请求头访问 API，同时支持携带凭证（如 Cookie）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源域访问
    allow_credentials=True,  # 允许携带身份凭证（如 Cookie、Authorization 等）
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET、POST、PUT、DELETE 等）
    allow_headers=["*"],  # 允许所有请求头
)

register_exception(app)
app.include_router(router=router, prefix="/api")


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()).replace("-", ""))

    token = _trace_id_var.set(trace_id)
    try:
        response = await call_next(request)
    finally:
        _trace_id_var.reset(token)

    cost_ms = round((time.time() - start_time) * 1000, 2)
    access_logger.info(
        f"method={request.method} path={request.url.path} status={response.status_code} cost={cost_ms}ms client={request.client.host}"
    )
    response.headers["X-Trace-ID"] = trace_id
    return response

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
