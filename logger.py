#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для логирования действий пользователей
"""

import logging
from datetime import datetime
import pytz
from sqlalchemy import select

from database import async_session_maker, User, UserAction
from texts import TEXTS, get_text

# Настройка часового пояса
from constants import TZ

logger = logging.getLogger(__name__)

async def log_user_action(user_id: int, action_type: str, action_data: str = None, message_text: str = None, 
                         reminder_day: int = None, reminder_type: str = None, reminder_date: datetime = None, 
                         is_final_reminder: bool = False, bot_deleted: bool = False):
    """Логирует действие пользователя в базу данных на русском языке"""
    async with async_session_maker() as session:
        try:
            # Получаем пользователя
            result = await session.execute(
                select(User).where(User.tg_id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Всегда записываем на русском языке
                russian_action_type = get_text("ru", f"action_{action_type}")
                
                # Переводим данные действия на русский язык
                russian_action_data = None
                if action_data:
                    # Проверяем, есть ли перевод для данных действия
                    action_data_key = f"action_data_{action_data}"
                    if action_data_key in TEXTS.get("ru", {}):
                        russian_action_data = get_text("ru", action_data_key)
                    else:
                        russian_action_data = action_data
                
                # Создаем запись о действии (время автоматически устанавливается в базе данных)
                action = UserAction(
                    user_id=user.id,
                    action_type=russian_action_type,
                    action_data=russian_action_data,
                    message_text=message_text,
                    reminder_day=reminder_day,
                    reminder_type=reminder_type,
                    reminder_date=datetime.now(TZ) if reminder_date is None else reminder_date.replace(tzinfo=TZ),
                    is_final_reminder=is_final_reminder,
                    bot_deleted=bot_deleted
                )
                session.add(action)
                await session.commit()
                
                logger.info(f"📝 Действие записано: User {user_id} | {russian_action_type} | {russian_action_data}")
            else:
                logger.warning(f"⚠️ Пользователь {user_id} не найден для логирования действия {action_type}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при логировании действия пользователя {user_id}: {e}")
