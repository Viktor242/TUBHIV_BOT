#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
База данных для хранения пользователей и их обследований
"""

import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с обследованиями
    cases = relationship("Case", back_populates="user")


class Case(Base):
    """Модель обследования/диагноза"""
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)  # Туберкулез, Сифилис, ВИЧ-инфекция, Наркомания
    registered_at = Column(DateTime, default=datetime.utcnow)
    deadline_at = Column(DateTime, nullable=False)  # Дата окончания 30 дней
    last_reminder_day = Column(Integer, default=0)  # День последнего напоминания (0, 5, 10, 15, 20, 25, 30)
    active = Column(Boolean, default=True)  # Активен ли случай
    completed = Column(Boolean, default=False)  # Завершен ли пользователем
    
    # Связь с пользователем
    user = relationship("User", back_populates="cases")


# Создаём движок и сессию
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных - создание таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Получить сессию базы данных"""
    async with async_session_maker() as session:
        yield session

