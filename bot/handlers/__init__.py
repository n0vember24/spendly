from . import start


def register_handlers(dp):
    dp.include_router(start.router)
