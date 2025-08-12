from bot.handlers import balance
from bot.handlers import start


def register_handlers(dp):
    dp.include_router(start.router)
    dp.include_router(balance.router)
