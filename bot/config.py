import os
import logging
from bot.utils import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN: logging.error('BOT_TOKEN does not exist')
