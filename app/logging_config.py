import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
FMT = "{asctime} [{levelname:^9}] {name}: {message}"

FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: "\33[33m" + FMT + "\33[0m",
    logging.ERROR: "\33[31m" + FMT + "\33[0m",
    logging.CRITICAL: "\33[1m\\33[31m" + FMT + "\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


def setup_logging():
    log_level = LOG_LEVEL
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(handler)
