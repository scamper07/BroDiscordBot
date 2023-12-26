import logging
import os

from logging.handlers import TimedRotatingFileHandler
from constants import LOG_FILE_LOCATION

# Create logs directory
if not os.path.exists("logs"):
    os.mkdir("logs")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(
    filename=LOG_FILE_LOCATION, when="midnight", backupCount=5
)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:[%(filename)s:%(lineno)d] %("
        "message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
)
logger.addHandler(handler)
