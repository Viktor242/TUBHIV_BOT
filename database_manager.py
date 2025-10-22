#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Менеджер базы данных - класс для работы с БД
"""

import logging
from datetime import datetime, timedelta
import pytz
from sqlalchemy import select
from database import async_session_maker, User, Activity
from texts import get_text, TEXTS

from constants import TZ

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Класс для управления операциями с базой данных"""
    
    def __init__(self):
        self.session_maker = async_session_maker
    
    async def log_user_action(self, user_id: int, action_type: str, action_data: str = None):
        """Логирует действие пользователя в базу данных на русском языке"""
        async with self.session_maker() as session:
            try:
                result = await session.execute(
                    select(User).where(User.tg_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if user:
                    russian_action_type = get_text("ru", f"action_{action_type}")
                    
                    russian_action_data = None
                    if action_data:
                        action_data_key = f"action_data_{action_data}"
                        if action_data_key in TEXTS.get("ru", {}):
                            russian_action_data = get_text("ru", action_data_key)
                        else:
                            russian_action_data = action_data
                    
                    action = Activity(
                        user_id=user.id,
                        action_type=russian_action_type,
                        action_data=russian_action_data
                    )
                    
                    session.add(action)
                    await session.commit()
                    
                    logger.info(f"📝 Действие записано: User {user_id} | {russian_action_type} | {russian_action_data}")
                else:
                    logger.warning(f"⚠️ Пользователь {user_id} не найден для логирования действия {action_type}")
                    
            except Exception as e:
                logger.error(f"❌ Ошибка при логировании действия пользователя {user_id}: {e}")
    
    async def get_user_by_tg_id(self, user_tg_id: int):
        """Получает пользователя по Telegram ID"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(User).where(User.tg_id == user_tg_id)
            )
            return result.scalar_one_or_none()
    
    async def update_user_language(self, user_tg_id: int, language: str):
        """Обновляет язык пользователя"""
        async with self.session_maker() as session:
            # Получаем пользователя в той же сессии
            result = await session.execute(
                select(User).where(User.tg_id == user_tg_id)
            )
            user = result.scalar_one_or_none()
            
            if user:
                user.language = language
                await session.commit()
                logger.info(f"Язык пользователя {user_tg_id} обновлен на {language}")
            else:
                logger.error(f"Пользователь {user_tg_id} не найден для обновления языка")
    
    async def get_user_activity(self, user_id: int):
        """Получает последнее действие пользователя"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(Activity).where(Activity.user_id == user_id).order_by(Activity.timestamp.desc())
            )
            return result.scalars().all()
    
    async def create_user(self, tg_id: int, username: str = None, name: str = None):
        """Создает нового пользователя"""
        async with self.session_maker() as session:
            try:
                # Устанавливаем deadline сразу при регистрации (30 дней до конца дня)
                now = datetime.now(TZ)
                # Устанавливаем дедлайн на конец 30-го дня (23:59:59)
                deadline = now.replace(hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=30)
                
                user = User(
                    tg_id=tg_id,
                    username=username,
                    name=name,  # Добавляем имя пользователя
                    language="ru",
                    deadline=deadline
                )
                session.add(user)
                await session.commit()
                logger.info(f"✅ Создан новый пользователь: {tg_id} с deadline: {deadline}")
                
                # Создаем задачи планировщика для напоминаний
                from scheduler import scheduler, send_regular_reminder, send_final_reminder, block_user_final
                
                # Первое напоминание через 1 минуту (для всех пользователей)
                scheduler.add_job(
                    send_regular_reminder,
                    "date",
                    run_date=datetime.now(TZ) + timedelta(minutes=1),
                    args=[user.tg_id, -1],  # -1 означает "через 1 минуту"
                    id=f"reminder_1m_{user.tg_id}",
                    replace_existing=True
                )
                
                # Напоминание через 5 часов (для всех пользователей)
                scheduler.add_job(
                    send_regular_reminder,
                    "date",
                    run_date=datetime.now(TZ) + timedelta(hours=5),
                    args=[user.tg_id, 0],  # 0 означает "через 5 часов"
                    id=f"reminder_5h_{user.tg_id}",
                    replace_existing=True
                )
                
                # Напоминания на 10, 20 дней
                reminder_days = [10, 20]
                for day in reminder_days:
                    scheduler.add_job(
                        send_regular_reminder,
                        "date",
                        run_date=datetime.now(TZ) + timedelta(days=day),
                        args=[user.tg_id, day],
                        id=f"reminder_{day}_{user.tg_id}",
                        replace_existing=True
                    )
                
                # Финальное напоминание на 30-й день
                scheduler.add_job(
                    send_final_reminder,
                    "date",
                    run_date=datetime.now(TZ) + timedelta(days=30),
                    args=[user.tg_id],
                    id=f"final_reminder_{user.tg_id}",
                    replace_existing=True
                )
                
                # Блокировка на 31-й день
                scheduler.add_job(
                    block_user_final,
                    "date",
                    run_date=datetime.now(TZ) + timedelta(days=31),
                    args=[user.tg_id],
                    id=f"block_final_{user.tg_id}",
                    replace_existing=True
                )
                
                return user
            except Exception as e:
                logger.error(f"❌ Ошибка при создании пользователя {tg_id}: {e}")
                return None
    
    async def get_user_status(self, user_tg_id: int):
        """Получает статус пользователя"""
        user = await self.get_user_by_tg_id(user_tg_id)
        if not user:
            return None
        
        activity = await self.get_user_activity(user.id)
        if not activity:
            return {"user": user, "activity": None}
        
        return {"user": user, "activity": activity[0]}
    
    async def log_reminder_sent(self, user_tg_id: int, reminder_day: int):
        """Записывает отправленное напоминание в activity"""
        async with self.session_maker() as session:
            try:
                user = await self.get_user_by_tg_id(user_tg_id)
                if not user:
                    logger.error(f"❌ Пользователь {user_tg_id} не найден для записи напоминания")
                    return False
                
                # Определяем тип напоминания
                if reminder_day == -1:  # -1 означает "через 1 минуту"
                    action_data = "1 минута"
                elif reminder_day == 0:
                    action_data = "5 часов"
                elif reminder_day == 30:
                    action_data = "30 дней (финальное)"
                elif reminder_day == 31:
                    action_data = "31 день (блокировка)"
                else:
                    action_data = f"{reminder_day} дней"
                
                # Создаем запись о напоминании
                activity = Activity(
                    user_id=user.id,
                    action_type="Напоминание отправлено",
                    action_data=action_data
                )
                
                session.add(activity)
                await session.commit()
                
                logger.info(f"✅ Записано напоминание {action_data} для пользователя {user_tg_id}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Ошибка при записи напоминания для {user_tg_id}: {e}")
                return False
    
    async def mark_reminder_sent(self, user_tg_id: int, reminder_type: str):
        """Отмечает отправленное уведомление в таблице users"""
        async with self.session_maker() as session:
            try:
                # Получаем пользователя в той же сессии
                result = await session.execute(
                    select(User).where(User.tg_id == user_tg_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    logger.error(f"❌ Пользователь {user_tg_id} не найден для отметки напоминания")
                    return False
                
                # Устанавливаем соответствующее поле в True
                if reminder_type == "1m":
                    user.reminder_1m = True
                elif reminder_type == "5h":
                    user.reminder_5h = True
                elif reminder_type == "10d":
                    user.reminder_10d = True
                elif reminder_type == "20d":
                    user.reminder_20d = True
                elif reminder_type == "30d":
                    user.reminder_30d = True
                else:
                    logger.error(f"❌ Неизвестный тип напоминания: {reminder_type}")
                    return False
                
                await session.commit()
                logger.info(f"✅ Отмечено напоминание {reminder_type} для пользователя {user_tg_id}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Ошибка при отметке напоминания для {user_tg_id}: {e}")
                return False
