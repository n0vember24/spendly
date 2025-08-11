import logging
import os

from bot.utils.dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_PATH: str = os.getenv('DB_PATH', 'spendly.db')
    DB_URL: str = os.getenv('DB_URL', 'sqlite+aiosqlite:///spendly.db')
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() in ('true', '1')


def validate_config():
    if not Config.BOT_TOKEN:
        raise ValueError('BOT_TOKEN is not set in .env')
    if not Config.DB_PATH:
        logging.warning('DB_PATH is not set, using `spendly.db` as default')
    if not Config.DB_URL:
        logging.warning('DB_URL is not set, using SQLITE:spendly.db as default')
