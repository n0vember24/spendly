from bot.handlers import balance
from bot.handlers import main


def register_handlers(dp):
    dp.include_router(main.router)
    dp.include_router(balance.router)
