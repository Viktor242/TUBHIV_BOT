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

    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")
    activity = relationship("Activity", back_populates="user", cascade="all, delete-orphan")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    registered_at = Column(DateTime, default=get_vladivostok_time)
    deadline_at = Column(DateTime, nullable=False)
    last_reminder_day = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    completed = Column(Boolean, default=False)
    expired = Column(Boolean, default=False)

    user = relationship("User", back_populates="cases")


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String, nullable=False)
    action_data = Column(String, nullable=True)
    message_text = Column(String, nullable=True)
    reminder_day = Column(Integer, nullable=True)
    reminder_type = Column(String, nullable=True)
    reminder_date = Column(DateTime, default=get_vladivostok_time)
    is_final_reminder = Column(Boolean, default=False)
    bot_deleted = Column(Boolean, default=False)
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
