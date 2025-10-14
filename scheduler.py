#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Планировщик напоминаний - проверяет каждый день, кому нужно отправить напоминание
"""

import os
import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from dotenv import load_dotenv

from database import async_session_maker, Case, User
from texts import REMINDER_TEMPLATE, FINAL_REMINDER

if TYPE_CHECKING:
    from aiogram import Bot

load_dotenv()

# Настройки
TZ = pytz.timezone(os.getenv("TZ", "Asia/Vladivostok"))
DAILY_REMINDER_HOUR = 22  # Принудительно 22:40 для тестирования СЕЙЧАС
DAILY_REMINDER_MINUTE = 40

logger = logging.getLogger(__name__)


async def check_reminders(bot: "Bot"):
    """
    Проверяет все активные обследования и отправляет напоминания по расписанию:
    - День 5, 10, 15, 20, 25 - обычные напоминания
    - День 30 - финальное напоминание
    """
    async with async_session_maker() as session:
        # Получаем все активные обследования
        result = await session.execute(
            select(Case, User)
            .join(User, Case.user_id == User.id)
            .where(Case.active == True)
        )
        cases_with_users = result.all()
        
        now = datetime.now(TZ)
        
        for case, user in cases_with_users:
            # Вычисляем количество дней с момента регистрации
            registered_at = case.registered_at.replace(tzinfo=TZ) if case.registered_at.tzinfo is None else case.registered_at
            days_passed = (now - registered_at).days
            
            # Определяем, нужно ли отправить напоминание
            reminder_days = [5, 10, 15, 20, 25, 30]
            
            for reminder_day in reminder_days:
                # Если прошло нужное количество дней и мы ещё не отправляли напоминание на этот день
                if days_passed >= reminder_day and case.last_reminder_day < reminder_day:
                    try:
                        # Отправляем напоминание
                        if reminder_day == 30:
                            # Финальное напоминание
                            message = FINAL_REMINDER.format(category=case.category)
                            # Деактивируем обследование
                            case.active = False
                        else:
                            # Обычное напоминание
                            remaining_days = 30 - days_passed
                            message = REMINDER_TEMPLATE.format(
                                days=days_passed,
                                category=case.category,
                                remaining=remaining_days
                            )
                        
                        await bot.send_message(user.tg_id, message)
                        
                        # Обновляем день последнего напоминания
                        case.last_reminder_day = reminder_day
                        await session.commit()
                        
                        logger.info(f"Отправлено напоминание пользователю {user.tg_id} на {reminder_day} день")
                        
                    except Exception as e:
                        logger.error(f"Ошибка при отправке напоминания пользователю {user.tg_id}: {e}")
                    
                    # Выходим из цикла, так как отправили напоминание
                    break


def setup_scheduler(bot: "Bot") -> AsyncIOScheduler:
    """
    Настраивает и запускает планировщик
    """
    scheduler = AsyncIOScheduler(timezone=TZ)
    
    # Запускаем проверку напоминаний каждый день в указанное время
    scheduler.add_job(
        check_reminders,
        trigger='cron',
        hour=DAILY_REMINDER_HOUR,
        minute=DAILY_REMINDER_MINUTE,
        args=[bot],
        id='daily_reminder_check',
        replace_existing=True
    )
    
    # Также можно добавить проверку каждые несколько часов для надёжности
    # scheduler.add_job(
    #     check_reminders,
    #     trigger='interval',
    #     hours=6,
    #     args=[bot],
    #     id='periodic_reminder_check',
    #     replace_existing=True
    # )
    
    scheduler.start()
    logger.info(f"Планировщик запущен. Проверка напоминаний каждый день в {DAILY_REMINDER_HOUR}:{DAILY_REMINDER_MINUTE:02d} ({TZ})")
    
    return scheduler

