from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import select, insert, update

from bot.db.engine import async_session
from bot.db.models import User, PlannedSpending, StatusEnum


async def add_planned(tg_id: int, title: str, amount: float, comment: Optional[str], remind_at: datetime) -> None:
    async with async_session() as session:
        q = await session.execute(select(User.balance).where(User.id == tg_id))
        balance = q.scalar_one_or_none()
        if not balance:
            raise RuntimeError(f'User {tg_id}: DATA IS NOT FOUND')
        await session.execute(
            insert(PlannedSpending)
            .values(user_id=tg_id, title=title, amount=amount, comment=comment, remind_at=remind_at))
        await session.execute(update(User).where(User.id == tg_id).values(balance=User.balance - amount))
        await session.commit()


async def get_planned(tg_id: int, limit: int = 50, offset: int = 0) -> Optional[List[PlannedSpending]]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        planned = await session.scalars(
            select(PlannedSpending)
            .where(PlannedSpending.user_id == user.id)
            .order_by(PlannedSpending.updated_at.desc())
            .limit(limit)
            .offset(offset))
        return planned.all()


async def get_all_planned(tg_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    async with async_session() as session:
        now = datetime.now()
        q = await session.execute(
            select(PlannedSpending)
            .where(PlannedSpending.user_id == tg_id)
            .where(PlannedSpending.status == StatusEnum.pending)
            .where(PlannedSpending.remind_at <= now)
            .order_by(PlannedSpending.remind_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return q.scalars()
