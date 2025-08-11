import logging
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, update
from bot.db.engine import async_session
from bot.db.models import User, Expense, PlannedExpense
from datetime import datetime


async def get_user_by_tg(tg_id: int) -> Optional[Dict[str, Any]]:
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.tg_id == tg_id))
            user = q.scalar_one_or_none()
            return user
    except Exception as exc:
        logging.error(exc)


async def create_user(tg_id: int, username: Optional[str], initial_balance: float = 0.0) -> None:
    try:
        async with async_session() as session:
            user = User(tg_id=tg_id, username=username, initial_balance=initial_balance)
            session.add(user)
            await session.commit()
            await session.refresh(user)
    except Exception as exc:
        logging.error(exc)


async def set_balance(tg_id: int, amount: float) -> None:
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.tg_id == tg_id))
            user = q.scalar_one_or_none()
            if not user:
                raise RuntimeError(f'User {tg_id} not found')
            user.initial_balance = amount
            await session.commit()
    except Exception as exc:
        logging.error(exc)


async def add_expense(tg_id: int, amount: float, comment: Optional[str]) -> None:
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.tg_id == tg_id))
            user = q.scalar_one_or_none()
            if not user:
                raise RuntimeError(f'User {tg_id} not found')
            expense = Expense(user_id=tg_id, amount=amount, comment=comment)
            session.add(expense)
            await session.commit()
            await session.refresh(expense)
    except Exception as exc:
        logging.error(exc)


async def get_expenses(tg_id: int, limit: int = 50) -> Optional[List[Dict[str, Any]]]:
    try:
        async with async_session() as session:
            q = await session.execute(select(User).where(User.tg_id == tg_id))
            user = q.scalar_one_or_none()
            if not user:
                raise RuntimeError(f'User {tg_id} not found')
            expenses = await session.execute(
                select(Expense).where(Expense.user_id == tg_id).order_by(Expense.created_at.desc()).limit(limit))
            total = expenses.scalars().all()
            return total
    except Exception as exc:
        logging.error(exc)
