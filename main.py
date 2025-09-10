import asyncio

from bot.core.config import validate_config
from bot.core.settings import bot, dp as dispatcher
from bot.handlers import register_handlers
from bot.utils.logger import setup_logger
from bot.middlewares import register_middlewares


async def main():
    setup_logger()
    validate_config()
    register_handlers(dispatcher)
    register_middlewares(dispatcher)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
