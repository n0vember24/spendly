from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, BigInteger, String, Float, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.engine import Base


class StatusEnum(PyEnum):
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.utcnow(),
        server_onupdate=func.now(),
        nullable=False)

    spendings = relationship('Spending', back_populates='user', cascade='all, delete-orphan')
    planned_spendings = relationship('PlannedSpending', back_populates='user', cascade='all, delete-orphan')


class Spending(Base):
    __tablename__ = 'spendings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.utcnow(),
        server_onupdate=func.now(),
        nullable=False)

    user = relationship('User', back_populates='spendings')


class PlannedSpending(Base):
    __tablename__ = 'planned_spendings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    remind_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name='status_enum'),
        default=StatusEnum.pending,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.utcnow(),
        server_onupdate=func.now(),
        nullable=False)

    user = relationship('User', back_populates='planned_spendings')
