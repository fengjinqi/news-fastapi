"""
@Author    : fengjinqi
@Time      : 2026/6/4 10:28 AM
@Email     : fengjinqi1204@gmail.com
@File      : setting.py
@Software  : PyCharm
"""
from pathlib import Path

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
    #Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: Optional[str] = None

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
settings = Settings()  # type: ignore[call-arg]
# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

# 日志基础配置
LOG_CONFIG = {
    "log_level": "DEBUG" if settings.ENV == "dev" else "INFO",
    "log_file_max_size": 50 * 1024 * 1024,  # 单文件50MB切割
    "log_file_backup_count": 10,  # 最多保留10个备份文件
    "console_log": True,          # 是否开启控制台打印
    "file_log": True,             # 是否开启文件落盘
}
