import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN, DEBUG
from bot.handlers.start import router


async def main(bot_token: str):
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode='markdown'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.WARNING)
        asyncio.run(main(BOT_TOKEN))
    except KeyboardInterrupt:
        logging.info('Shutdown.')
    except Exception as exc:
        logging.error(exc)
