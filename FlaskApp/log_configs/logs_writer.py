import os
import sys
import logging

__all__ = ['logger']


log_file_name = "FlaskApp_logs.log"
log_file_path = "/var/log/flask/"

log_file_abs_path = os.path.join(log_file_path, log_file_name)

# Creating the log directory if not exists
os.makedirs(os.path.dirname(log_file_abs_path), exist_ok=True)

file_handler = logging.FileHandler(filename=log_file_abs_path)
console_handler = logging.StreamHandler(stream=sys.stdout)

log_level = logging.DEBUG
log_format = "[%(asctime)s] [%(levelname)s] [%(filename)s @%(lineno)d | %(funcName)s]  %(message)s"

file_formatter = logging.Formatter(log_format)
console_formatter = logging.Formatter(log_format)

file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

file_handler.setLevel(log_level)
console_handler.setLevel(log_level)

logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
