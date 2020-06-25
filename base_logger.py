import logging
import os

from logging.handlers import TimedRotatingFileHandler

# Create logs directory
if not os.path.exists('logs'):
    os.mkdir('logs')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(filename='logs/discord.log', when="midnight", backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
logger.addHandler(handler)