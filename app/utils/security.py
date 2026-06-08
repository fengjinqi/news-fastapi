"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:24 AM
@Email     : fengjinqi1204@gmail.com
@File      : __init__.py.py
@Software  : PyCharm
"""
from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    加密密码
    :param password:
    :return:
    """
    return pwd_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_hash.verify(plain_password, hashed_password)
