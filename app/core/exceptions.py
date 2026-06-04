"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.response import resp_error
import logging

logger = logging.getLogger(__name__)



class AppBizException(Exception):
    def __init__(self, code: int = 400, msg: str = "业务异常"):
        self.code = code
        self.msg = msg

async def biz_exception_handler(request: Request, exc: AppBizException):
    result = resp_error(code=exc.code, message=exc.msg)
    return JSONResponse(content=result.model_dump(), status_code=exc.code)

async def http_exception_handler(request: Request, exc: HTTPException):
    result = resp_error(code=exc.status_code, message=exc.detail)
    return JSONResponse(content=result.model_dump(), status_code=exc.status_code)

async def validate_exception_handler(request: Request, exc: RequestValidationError):
    err_info = [f"{e['loc']}:{e['msg']}" for e in exc.errors()]
    result = resp_error(code=422, message=f"参数错误:{err_info}")
    return JSONResponse(content=result.model_dump(), status_code=422)

async def sql_exception_handler(request: Request, exc: SQLAlchemyError):
    result = resp_error(code=500, message="数据库操作异常")
    return JSONResponse(content=result.model_dump(), status_code=500)

async def global_exception_handler(request: Request, exc: Exception):
    result = resp_error(code=500, message="服务器未知异常")
    return JSONResponse(content=result.model_dump(), status_code=500)

def register_exception(app):
    app.add_exception_handler(AppBizException, biz_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validate_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sql_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

