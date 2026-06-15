"""
@Author    : fengjinqi
@Time      : 2026/6/15
@Email     : fengjinqi1204@gmail.com
@File      : logger.py
@Software  : PyCharm
"""
import logging
import os
import sys
from contextvars import ContextVar
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from app.config.setting import LOG_DIR, LOG_CONFIG

# 日志格式化模板
_trace_id_var: ContextVar[str] = ContextVar("trace_id", default="00000000000000000000000000000000")

# asctime:时间 levelname:级别 process:进程 threadName:线程 trace_id:链路ID name:模块 message:日志内容 exc_info:异常栈
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(process)d | %(threadName)s | trace_id:%(trace_id)s | %(name)s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 给日志record增加默认trace_id字段，防止无链路时报错
class TraceFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = _trace_id_var.get()
        return True

def setup_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_CONFIG["log_level"])
    root_logger.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    trace_filter = TraceFilter()

    if LOG_CONFIG["console_log"]:
        console_handler = StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(trace_filter)
        root_logger.addHandler(console_handler)

    if LOG_CONFIG["file_log"]:
        backup_cnt = LOG_CONFIG["log_file_backup_count"]

        all_file = os.path.join(LOG_DIR, "all.log")
        all_handler = TimedRotatingFileHandler(
            all_file, when="midnight", backupCount=backup_cnt, encoding="utf-8"
        )
        all_handler.suffix = "%Y-%m-%d"
        all_handler.setFormatter(formatter)
        all_handler.addFilter(trace_filter)
        root_logger.addHandler(all_handler)

        error_file = os.path.join(LOG_DIR, "error.log")
        error_handler = TimedRotatingFileHandler(
            error_file, when="midnight", backupCount=backup_cnt, encoding="utf-8"
        )
        error_handler.suffix = "%Y-%m-%d"
        error_handler.setFormatter(formatter)
        error_handler.addFilter(trace_filter)
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)

        access_file = os.path.join(LOG_DIR, "access.log")
        access_handler = TimedRotatingFileHandler(
            access_file, when="midnight", backupCount=backup_cnt, encoding="utf-8"
        )
        access_handler.suffix = "%Y-%m-%d"
        access_handler.setFormatter(formatter)
        access_handler.addFilter(trace_filter)
        access_logger = logging.getLogger("access")
        access_logger.handlers.clear()
        access_logger.addHandler(access_handler)
        access_logger.propagate = False

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)



# 全局日志获取函数
def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    return logger

# 初始化执行
setup_logger()
logger = get_logger("app")
access_logger = get_logger("access")