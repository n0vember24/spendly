from typing import Optional

from sqlalchemy import select, update, insert, exists

from bot.db.engine import async_session
from bot.db.models import User, PlannedSpending


async def get_user(tg_id: int) -> Optional[User]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        return user


async def if_exists(tg_id: int) -> bool:
    async with async_session() as session:
        q = await session.execute(select(exists().where(User.id == tg_id)).limit(1))
        return bool(q.scalar_one_or_none())


async def create_user(tg_id: int, username: Optional[str], balance: float = 0.0) -> None:
    async with async_session() as session:
        await session.execute(insert(User).values(id=tg_id, username=username, balance=balance))
        await session.commit()


async def mark_planned_done(planned_id: int) -> None:
    async with async_session() as session:
        await session.execute(update(PlannedSpending).where(PlannedSpending.id == planned_id).values(status='done'))
        await session.commit()
