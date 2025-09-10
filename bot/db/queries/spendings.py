from typing import Optional, List

from sqlalchemy import select, func, insert, update

from bot.db.engine import async_session
from bot.db.models import User, Spending


async def add_spending(tg_id: int, title: str, amount: float, comment: Optional[str] = '') -> None:
    async with async_session() as session:
        q = await session.execute(select(User.balance).where(User.id == tg_id))
        balance = q.scalar_one_or_none()
        if not balance:
            raise RuntimeError(f'User {tg_id}: DATA IS NOT FOUND')
        if balance < amount:
            raise RuntimeError(f'User {tg_id}: NOT ENOUGH BALANCE TO PERFORM OPERATION')
        await session.execute(insert(Spending).values(user_id=tg_id, title=title, amount=amount, comment=comment))
        await session.execute(update(User).where(User.id == tg_id).values(balance=User.balance - amount))
        await session.commit()


async def get_spendings(tg_id: int, limit: int = 50, offset: int = 0) -> Optional[List[Spending]]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id}: DATA IS NOT FOUND')
        spendings = await session.scalars(
            select(Spending)
            .where(Spending.user_id == tg_id)
            .order_by(Spending.updated_at.desc())
            .limit(limit)
            .offset(offset))
        return spendings.all()


async def get_spendings_sum(tg_id: int) -> Optional[float]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            return 0.0
        res = await session.execute(
            select(func.coalesce(func.sum(Spending.amount), 0)).where(Spending.user_id == tg_id))
        total = res.scalar_one()
        return float(total or 0.0)
