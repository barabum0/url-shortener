import logging
import sys

from loguru import logger

from url_shortener.tools.logs.handlers import UvicornHandler


def configure_logger():
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    logger.remove()
    logger.add(
        sys.stdout, colorize=True, format=log_format, diagnose=True, backtrace=False
    )
    logger.add(
        "log.log",
        rotation="1 week",
        diagnose=True,
        enqueue=True,
        colorize=True,
        backtrace=True,
    )
    logger.level("DEBUG", color="<fg #7f7f7f>")
    logger.level("INFO", color="<white>")
    logger.level("SUCCESS", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<red>")
    logger.level("CRITICAL", color="<bold><white><RED>")
    logger.level("REQUEST", no=38, color="<blue>")


def get_uvicorn_log_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
        },
        "handlers": {
            "default": {
                "()": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "uvicorn": {
                "()": "url_shortener.tools.logs.handlers.UvicornHandler",
            },
            "uvicorn.error": {
                "()": "url_shortener.tools.logs.handlers.UvicornHandler",
            },
            "uvicorn.access": {
                "()": "url_shortener.tools.logs.handlers.UvicornHandler",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["uvicorn"], "level": "INFO"},
            "uvicorn.error": {"handlers": ["uvicorn.error"], "level": "INFO"},
            "uvicorn.access": {"handlers": ["uvicorn.access"], "level": "INFO"},
        },
    }