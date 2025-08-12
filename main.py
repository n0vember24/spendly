import asyncio

from bot.core.bot import bot, dp
from bot.core.config import validate_config
from bot.handlers import register_handlers
from bot.utils.logger import setup_logger
from bot.db.engine import engine, Base


async def main():
    setup_logger()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    validate_config()
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
