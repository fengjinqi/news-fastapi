"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:28 AM
@Email     : fengjinqi1204@gmail.com
@File      : settungs.py
@Software  : PyCharm
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"), env_file_encoding="utf-8")
    # 项目
    ENV: str = "dev"
    PROJECT_NAME: str
    API_PREFIX: str
    # 数据库
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
if __name__ == '__main__':
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
