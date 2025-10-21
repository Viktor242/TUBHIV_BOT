#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""База данных для хранения пользователей, обследований и активности (напоминаний)"""

import os
from datetime import datetime
import pytz
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

load_dotenv()

TZ = pytz.timezone("Asia/Vladivostok")

def get_vladivostok_time():
    return datetime.now(TZ)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    language = Column(String, default="ru")
    created_at = Column(DateTime, default=get_vladivostok_time)
    blocked = Column(Boolean, default=False)
    
    # Срок окончания обследования (30 дней с момента выбора диагноза)
    deadline = Column(DateTime, nullable=True)
    
    # Отметки о отправленных уведомлениях
    reminder_1m = Column(Boolean, default=False)    # Напоминание через 1 минуту
    reminder_5h = Column(Boolean, default=False)    # Напоминание через 5 часов
    reminder_10d = Column(Boolean, default=False) # Напоминание через 10 дней
    reminder_20d = Column(Boolean, default=False) # Напоминание через 20 дней
    reminder_30d = Column(Boolean, default=False) # Финальное напоминание через 30 дней

    activity = relationship("Activity", back_populates="user", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String, nullable=False)
    action_data = Column(String, nullable=True)
    timestamp = Column(DateTime, default=get_vladivostok_time)

    user = relationship("User", back_populates="activity")


engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
