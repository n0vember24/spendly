from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import select, func, update

from bot.db.engine import async_session
from bot.db.models import User, Expense, PlannedExpense, StatusEnum


async def get_user_by_tg(tg_id: int) -> Optional[User]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user = q.scalar_one_or_none()
        return user


async def create_user(tg_id: int, username: Optional[str], balance: float = 0.0) -> None:
    async with async_session() as session:
        user = User(tg_id=tg_id, username=username, balance=balance)
        session.add(user)
        await session.commit()
        await session.refresh(user)


async def set_balance(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        user.balance = amount
        await session.commit()


async def add_balance(tg_id: int, amount: float) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        user.balance = + amount
        await session.commit()


async def add_expense(tg_id: int, amount: float, comment: Optional[str]) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user: Optional[User] = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        expense = Expense(user_id=user.id, amount=amount, comment=comment)
        session.add(expense)
        await session.commit()
        await session.refresh(expense)


async def get_expenses(tg_id: int, limit: int = 50) -> Optional[List[Dict[str, Any]]]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user: Optional[User] = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        expenses = await session.execute(
            select(Expense).where(Expense.user_id == user.id).order_by(Expense.created_at.desc()).limit(limit))
        total = expenses.scalars().all()
        return total


async def get_sum_expenses(tg_id: int) -> Optional[float]:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            return 0.0
        res = await session.execute(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.user_id == tg_id))
        total = res.scalar_one()
        return float(total or 0.0)


async def add_planned(tg_id: int, amount: float, comment: Optional[str], remind_at: datetime) -> None:
    async with async_session() as session:
        q = await session.execute(select(User).where(User.tg_id == tg_id))
        user = q.scalar_one_or_none()
        if not user:
            raise RuntimeError(f'User {tg_id} not found')
        p = PlannedExpense(user_id=tg_id, amount=amount, comment=comment, remind_at=remind_at)
        session.add(p)
        await session.commit()


async def get_planned() -> List[Dict[str, Any]]:
    async with async_session() as session:
        now = datetime.now()
        res = await session.execute(
            select(PlannedExpense, User.tg_id)
            .join(User, PlannedExpense.user_id == User.id)
            .where(PlannedExpense.status == StatusEnum.pending)
            .where(PlannedExpense.remind_at <= now)
            .order_by(PlannedExpense.remind_at.asc())
        )
        rows = res.all()
        return rows


async def mark_planned_done(planned_id: int) -> None:
    async with async_session() as session:
        await session.execute(update(PlannedExpense).where(PlannedExpense.id == planned_id).values(status='done'))
        await session.commit()
