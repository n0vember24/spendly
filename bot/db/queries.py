from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import select, func, update, insert

from bot.db.engine import async_session
from bot.db.models import User, Spending, PlannedSpending, StatusEnum


async def get_user(tg_id: int) -> Optional[User]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        return user


async def create_user(tg_id: int, username: Optional[str], balance: float = 0.0) -> None:
    async with async_session() as session:
        await session.execute(insert(User).values(id=tg_id, username=username, balance=balance))
        await session.commit()


async def set_balance(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        user.balance = amount
        await session.commit()


async def add_balance(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        user.balance = + amount
        await session.commit()


async def add_spending(tg_id: int, title: str, amount: float, comment: Optional[str]) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user: Optional[User] = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        if user.balance < amount:
            raise RuntimeError(f'User({tg_id})\'s balance is not enough for creating this spending.\n'
                               f'Balance: {user.balance}\nSpending: {amount}')
        spending = Spending(user_id=user.id, title=title, amount=amount, comment=comment)
        user.balance -= amount
        session.add(spending)
        await session.commit()


async def get_spendings(tg_id: int, limit: int = 50) -> Optional[List[Spending]]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user: Optional[User] = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        spendings = await session.scalars(
            select(Spending).where(Spending.user_id == user.id).order_by(Spending.updated_at.desc()).limit(limit))
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


async def add_planned(tg_id: int, title: str, amount: float, comment: Optional[str], remind_at: datetime) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        p = PlannedSpending(user_id=tg_id, title=title, amount=amount, comment=comment, remind_at=remind_at)
        session.add(p)
        await session.commit()


async def get_planned(tg_id: int, limit: int = 50) -> Optional[List[PlannedSpending]]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.id == tg_id))
        user: Optional[User] = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        planned = await session.scalars(
            select(PlannedSpending)
            .where(PlannedSpending.user_id == user.id)
            .order_by(PlannedSpending.updated_at.desc())
            .limit(limit))
        return planned.all()


async def get_all_planned() -> List[Dict[str, Any]]:
    async with async_session() as session:
        now = datetime.now()
        res = await session.execute(
            select(PlannedSpending, User.id)
            .join(User, PlannedSpending.user_id == User.id)
            .where(PlannedSpending.status == StatusEnum.pending)
            .where(PlannedSpending.remind_at <= now)
            .order_by(PlannedSpending.remind_at.asc())
        )
        rows = res.all()
        return rows


async def mark_planned_done(planned_id: int) -> None:
    async with async_session() as session:
        await session.execute(update(PlannedSpending).where(PlannedSpending.id == planned_id).values(status='done'))
        await session.commit()
