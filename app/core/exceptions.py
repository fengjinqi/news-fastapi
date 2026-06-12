"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
import traceback

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.response import resp_error
from app.utils.logger import get_logger


logger = get_logger(__name__)


def _fmt_request(request: Request) -> str:
    return (
        f"{request.method} {request.url.path}"
        f" | query={dict(request.query_params)}"
        f" | client={request.client.host if request.client else 'unknown'}"
    )
class AppBizException(Exception):
    def __init__(self, code: int = 400, msg: str = "业务异常"):
        self.code = code
        self.msg = msg

async def biz_exception_handler(request: Request, exc: AppBizException):
    result = resp_error(code=exc.code, message=exc.msg)
    logger.error(f"业务异常:[{_fmt_request(request)}] {exc.code} - {exc.msg}")
    return JSONResponse(content=result.model_dump(), status_code=exc.code)

async def http_exception_handler(request: Request, exc: HTTPException):
    result = resp_error(code=exc.status_code, message=exc.detail)
    logger.error(f"HTTP异常:[{_fmt_request(request)}] {exc.status_code} - {exc.detail}")
    return JSONResponse(content=result.model_dump(), status_code=exc.status_code)

async def validate_exception_handler(request: Request, exc: RequestValidationError):
    err_info = [f"{e['loc']}:{e['msg']}" for e in exc.errors()]
    result = resp_error(code=422, message=f"参数错误:{err_info}")
    logger.error(f"参数验证异常:[{_fmt_request(request)}]{err_info}")
    return JSONResponse(content=result.model_dump(), status_code=422)

async def sql_exception_handler(request: Request, exc: SQLAlchemyError):
    result = resp_error(code=500, message=f"数据库操作异常:{exc}")
    logger.error(f"数据库异常:[{_fmt_request(request)}] {exc}")
    return JSONResponse(content=result.model_dump(), status_code=500)

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"服务器未知异常:[{_fmt_request(request)}] {traceback.format_exc()}")
    logger.error(f"服务器未知异常:[{_fmt_request(request)}] {exc}")
    result = resp_error(code=500, message=f"服务器未知异常")
    return JSONResponse(content=result.model_dump(), status_code=500)
async def value_error_handler(request: Request, exc: ValueError):
    result = resp_error(code=400, message=f"{exc}")
    logger.error(f"值错误:[{_fmt_request(request)}] {exc}")
    return JSONResponse(content=result.model_dump(), status_code=400)

def register_exception(app):
    app.add_exception_handler(AppBizException, biz_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validate_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sql_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)



