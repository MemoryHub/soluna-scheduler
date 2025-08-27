import os
from loguru import logger

# 获取日志级别
log_level = os.getenv('LOG_LEVEL', 'INFO')

# 移除默认的日志处理器
logger.remove()

# 添加控制台日志处理器
logger.add(
    sink=lambda msg: print(msg, end=""),
    level=log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True
)

# 添加文件日志处理器
logger.add(
    "scheduler.log",
    rotation="1 day",  # 每天轮换
    retention="30 days",  # 保留30天
    level=log_level,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8"
)

# 导出logger供其他模块使用
global_logger = logger