"""
@Author    : fengjinqi
@Time      : 2026/6/15
@Email     : fengjinqi1204@gmail.com
@File      : logger.py
@Software  : PyCharm
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from app.config.setting import settings

LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "logs",
)
os.makedirs(LOG_DIR, exist_ok=True)

_LOG_LEVEL = logging.DEBUG if settings.ENV == "dev" else logging.INFO

_FORMATTER = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _build_console_handler() -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(_LOG_LEVEL)
    handler.setFormatter(_FORMATTER)
    return handler


def _build_file_handler() -> TimedRotatingFileHandler:
    handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "app.log"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    handler.setLevel(_LOG_LEVEL)
    handler.setFormatter(_FORMATTER)
    handler.suffix = "%Y-%m-%d"
    return handler


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(_LOG_LEVEL)
        logger.addHandler(_build_console_handler())
        logger.addHandler(_build_file_handler())
        logger.propagate = False
    return logger