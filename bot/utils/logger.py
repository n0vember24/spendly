import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from bot.core.config import Config


def setup_logger(base_log_dir: str = 'logs'):
    now = datetime.now()
    log_dir = os.path.join(base_log_dir, now.strftime('%Y'), now.strftime('%m'))
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'{now.strftime('%d')}.log')

    logger = logging.getLogger()
    log_level = logging.DEBUG if Config.DEBUG else logging.INFO
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = TimedRotatingFileHandler(log_file, 'midnight', 1, 30, 'utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info('-' * 50)
    logging.debug('Logger is initialized')
