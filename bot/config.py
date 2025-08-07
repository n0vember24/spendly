import os
import logging
from bot.utils import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEBUG = os.getenv('DEBUG', 'false').lower() in ('true', '1')

if not BOT_TOKEN: logging.error('BOT_TOKEN does not exist')
