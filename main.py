import asyncio

from bot.core.bot import bot, dp
from bot.core.config import validate_config
from bot.handlers import register_handlers
from bot.utils.logger import setup_logger


async def main():
    setup_logger()
    validate_config()
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
