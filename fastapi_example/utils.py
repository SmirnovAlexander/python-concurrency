import logging
import sys
from itertools import chain
from types import FrameType
from typing import cast

import uvicorn
from loguru import logger
from uvicorn.supervisors import ChangeReload, Multiprocess

# logger.add(f"{CONFIG['app']['log_path']}")
my_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <magenta>{process.name: <18}</magenta> | <magenta>{thread.name: <12}</magenta> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.remove()
logger.add(sys.stderr, format=my_format)


class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging module"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_loguru_logging_intercept(level=logging.DEBUG, modules=()):
    logging.basicConfig(handlers=[InterceptHandler()], level=level)  # noqa
    for logger_name in chain(("",), modules):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def run_uvicorn_loguru(config: uvicorn.Config, force_exit=False):
    """Same as uvicorn.run but injects loguru logging"""
    server = uvicorn.Server(config=config)
    server.force_exit = force_exit
    setup_loguru_logging_intercept(
        level=logging.getLevelName(config.log_level.upper()),
        modules=("uvicorn.error", "uvicorn.asgi", "uvicorn.access"),
    )
    supervisor_type = None
    if config.should_reload:
        supervisor_type = ChangeReload
    if config.workers > 1:
        supervisor_type = Multiprocess
    if supervisor_type:
        sock = config.bind_socket()
        supervisor = supervisor_type(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()
