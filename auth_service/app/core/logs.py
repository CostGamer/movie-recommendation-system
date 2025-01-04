import logging
import sys

from pythonjsonlogger import jsonlogger

from app.core.config import LoggingSettings

logger = logging.getLogger(__name__)


def init_logger(log_settings: LoggingSettings) -> None:
    log_level = log_settings.log_level.upper()
    log_file = log_settings.log_file
    log_encoding = log_settings.log_encoding
    log_format = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"

    formatter = jsonlogger.JsonFormatter(log_format)
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file, encoding=log_encoding)
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[stream_handler, file_handler])
