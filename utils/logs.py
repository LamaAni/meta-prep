import os
import logging
from typing import Union
from bole.log import (
    BoleLogFormatter,
    create_random_string,
    resolve_log_level,
    BOLE_LOG_FORMAT_EXTRA_INFO,
)

REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LOG_FORMAT: str = "".join(
    [
        "[%(gray)s%(timestamp)s%(end_color)s][%(levelcolor)s%(levelname)5s%(end_color)s][%(name)s]",
        BOLE_LOG_FORMAT_EXTRA_INFO,
        " %(msg)s",
    ]
)


def create_logger(
    logger_name: str = None,
    log_level: Union[str, int] = None,
    log_format: str = LOG_FORMAT,
):
    """Create a new bole logger, given a logger name.

    Args:
        logger_name (str, optional): The name of the new logger. Defaults to None.
        log_level (Union[str, int], optional): Logger log level. Defaults to None.

    Returns:
        Logger: The new logger
    """
    logger_name = logger_name or "bole-log-" + create_random_string()
    log = logging.Logger(logger_name)

    log_level = resolve_log_level(log_level or os.environ.get("LOG_LEVEL", "INFO"))
    log.setLevel(log_level)

    formatter = BoleLogFormatter(log_format=log_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
