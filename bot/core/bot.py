from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import Config

bot = Bot(Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode='markdown'))
dp = Dispatcher()
