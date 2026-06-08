"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.jwt import create_refresh_token, decode_access_token, create_access_token
from app.core.response import ResponseModel, resp_error, resp_success

from app.models.users import User

from app.schems.user import UserRegisterRequest, UserResponse, UserLogin, UserRequest
from app.services import users_service
from app.utils.deps import get_current_user

router = APIRouter(prefix="/user", tags=["用户"])


@router.post("")
async def create_user(param: UserRegisterRequest, db: AsyncSession = Depends(get_db), ) -> ResponseModel:
    """
    创建用户
    :param param: 用户参数
    :param db: 数据库会话
    :return: 创建的用户
    """
    username = await users_service.get_by_username(db, param.username)
    if username:
        return resp_error(code=400, message="用户名已存在")
    user = await users_service.create(db, param)
    return resp_success(message="用户创建成功")


@router.post("/login", summary="用户登录")
async def login(param: UserLogin, db: AsyncSession = Depends(get_db)) -> ResponseModel:
    user = await users_service.login(db, param.username, param.password)
    if user is None:
        return resp_error(code=401, message="用户名或密码错误")
    access_token = create_access_token(data={"sub": str(user.id)})

    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return resp_success(data={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"},
                        message="登录成功")


@router.post("/login/form", summary="用户登录")
async def login_form(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await users_service.login(db, form.username, form.password)
    if user is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)) -> ResponseModel:
    payload = decode_access_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        return resp_error(code=401, message="无效的refresh_token")
    user_id = int(payload.get("sub"))
    user = await users_service.read(db, user_id)
    if user is None:
        return resp_error(code=401, message="用户不存在")
    new_token = create_access_token(data={"sub": str(user.id)})
    return resp_success(data={"access_token": new_token, "token_type": "bearer"})


@router.get("/info", response_model=ResponseModel, summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)) -> ResponseModel:
    return resp_success(data=UserResponse.model_validate(current_user).model_dump())


@router.put("/{id}", response_model=ResponseModel, summary="更新当前用户信息",dependencies=[Depends(get_current_user)])
async def update_me(param: UserRequest, id: Annotated[int, Path(gt=0, description="用户ID")], db: AsyncSession = Depends(get_db)) -> ResponseModel:
    user = await users_service.update(db,id, param)
    if user is None:
        return resp_error(code=400, message="用户更新失败")
    return resp_success(message="用户更新成功")
