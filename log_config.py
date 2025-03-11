from loguru import logger
import sys
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger.remove()

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}"

logger.add(sys.stdout, level="DEBUG", format=LOG_FORMAT)
logger.add(f"{LOG_DIR}/app.log", rotation="10 MB", level="DEBUG", format=LOG_FORMAT)

def get_logger(name):
    return logger.bind(module=name)
