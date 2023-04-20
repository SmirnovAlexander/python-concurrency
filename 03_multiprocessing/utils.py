import sys

from loguru import logger

my_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <magenta>{process.name: <15}</magenta> | <magenta>{thread.name: <12}</magenta> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.remove()
logger.add(sys.stderr, format=my_format)
