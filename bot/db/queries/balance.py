from typing import Optional

from sqlalchemy import select, update

from bot.db.engine import async_session
from bot.db.models import User


async def deposit(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.id == tg_id)
            .values(balance=User.balance + amount)
            .returning(User.id))
        await session.commit()


async def set_balance(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.id == tg_id)
            .values(balance=amount)
            .returning(User.id))
        await session.commit()


async def get_balance(tg_id: int) -> Optional[float]:
    async with async_session() as session:
        q = await session.execute(select(User.balance).where(User.id == tg_id))
        return q.scalar_one_or_none()
