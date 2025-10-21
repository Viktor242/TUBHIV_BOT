#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Планировщик напоминаний и финальных уведомлений"""

import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from database import async_session_maker, User, Activity
from texts import get_text
from sqlalchemy import update

from constants import TZ
DAILY_REMINDER_HOUR = 9
DAILY_REMINDER_MINUTE = 30

logger = logging.getLogger(__name__)

# Глобальная переменная для бота (будет установлена при запуске)
bot = None
scheduler = None

def set_bot(bot_instance):
    """Устанавливает экземпляр бота для использования в планировщике"""
    global bot
    bot = bot_instance

async def send_expiration_warning(user_id: int):
    """Отправляет уведомление о завершении срока обследования"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text="⚠️ ВНИМАНИЕ! Сроки по дообследованию закончены. Ваши документы поданы в миграционную службу."
        )
        logger.info(f"📨 Уведомление о завершении срока отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления пользователю {user_id}: {e}")

async def check_reminders(bot):
    """Проверка и отправка напоминаний пользователям"""
    async with async_session_maker() as session:
        # Ищем всех пользователей с активными обследованиями
        result = await session.execute(
            select(User)
            .where(User.created_at.isnot(None))
        )
        users = result.scalars().all()
        now = datetime.now(TZ)

        for user in users:
            try:
                # Вычисляем дни с момента регистрации
                reg = user.created_at.replace(tzinfo=TZ)
                days_passed = (now.date() - reg.date()).days
                
                # Напоминания отправляем на 1 минута, 10, 20, 30 дни
                reminder_days = [10, 20, 30]
                
                for rd in reminder_days:
                    if days_passed >= rd:
                        # Проверяем, было ли уже отправлено напоминание на этот день
                        existing_reminder = await session.execute(
                            select(Activity)
                            .where(
                                Activity.user_id == user.id,
                                Activity.reminder_day == rd,
                                Activity.action_type == "reminder_sent"
                            )
                        )
                        
                        if existing_reminder.scalar_one_or_none() is None:
                            # Отправляем напоминание
                            registered = reg.strftime("%d.%m.%Y")
                            remaining = max(0, 30 - days_passed)
                            
                            if rd < 30:
                                text = (
                                    f"⏰ Напоминание о дообследовании\n\n"
                                    f"Дата регистрации: {registered}\n"
                                    f"Прошло дней: {days_passed}\n"
                                    f"Осталось дней: {remaining}\n\n"
                                    f"Не забудьте пройти обследование вовремя!"
                                )
                                reminder_type = "regular"
                            else:
                                # 30-й день - финальное напоминание
                                text = get_text(user.language, "final_reminder")
                                reminder_type = "final"

                            await bot.send_message(user.tg_id, text)
                            
                            # Записываем отправленное напоминание
                            reminder_activity = Activity(
                                user_id=user.id,
                                action_type="Напоминание отправлено",
                                action_data=f"{rd} дней"
                            )
                            session.add(reminder_activity)
                            await session.commit()
                            logger.info(f"✅ Напоминание {rd}-й день отправлено пользователю {user.tg_id}")
                            break  # Отправляем только одно напоминание за раз
                            
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомления пользователю {user.tg_id}: {e}")

async def cleanup_users_after_31_days(bot):
    """Отправка финального сообщения и деактивация пользователей через 31 день"""
    async with async_session_maker() as session:
        now = datetime.now(TZ)
        cutoff = now - timedelta(days=31)

        # Находим пользователей, которые зарегистрированы более 31 дня назад
        # и получили финальное напоминание на 30-й день
        result = await session.execute(
            select(User)
            .where(User.created_at < cutoff)
        )
        
        users = result.scalars().all()
        
        for user in users:
            try:
                # Проверяем, что пользователь получил финальное напоминание на 30-й день
                activity_result = await session.execute(
                    select(Activity)
                    .where(
                        Activity.user_id == user.id,
                        Activity.reminder_day == 30,
                        Activity.is_final_reminder == True
                    )
                )
                
                final_reminder = activity_result.scalar_one_or_none()
                
                # Если финальное напоминание было отправлено, отправляем сообщение о ликвидации
                if final_reminder:
                    text = get_text(user.language, "bot_liquidation_message")
                    await bot.send_message(user.tg_id, text)
                    
                    # Записываем активность о ликвидации бота
                    liquidation_activity = Activity(
                        user_id=user.id,
                        action_type="Бот заблокирован",
                        action_data="31 день"
                    )
                    session.add(liquidation_activity)
                    await session.commit()
                    logger.info(f"🚫 Финальное сообщение о ликвидации отправлено пользователю {user.tg_id}")
                    
            except Exception as e:
                logger.error(f"Ошибка при отправке финального уведомления {user.tg_id}: {e}")

# ====== 🔔 РАБОЧИЕ ФУНКЦИИ НАПОМИНАНИЙ ======

def get_time_text(language: str, time_type: str) -> str:
    """Возвращает правильный текст времени для каждого языка"""
    time_texts = {
        "ru": {
            "1m": "1 минута прошла",
            "5h": "5 часов прошло", 
            "10d": "10 дней прошло",
            "20d": "20 дней прошло",
            "30d": "30 дней прошло"
        },
        "uz": {
            "1m": "1 daqiqa o'tdi",
            "5h": "5 soat o'tdi",
            "10d": "10 kun o'tdi",
            "20d": "20 kun o'tdi", 
            "30d": "30 kun o'tdi"
        },
        "zh": {
            "1m": "1 分钟已过",
            "5h": "5 小时已过",
            "10d": "10 天已过",
            "20d": "20 天已过",
            "30d": "30 天已过"
        },
        "ko": {
            "1m": "1분 경과",
            "5h": "5시간 경과",
            "10d": "10일 경과",
            "20d": "20일 경과",
            "30d": "30일 경과"
        },
        "en": {
            "1m": "1 minute has passed",
            "5h": "5 hours have passed",
            "10d": "10 days have passed",
            "20d": "20 days have passed",
            "30d": "30 days have passed"
        }
    }
    
    return time_texts.get(language, time_texts["ru"]).get(time_type, f"{time_type}")


async def send_regular_reminder(user_id: int, day: int):
    """Отправляет обычное напоминание (через 5 часов, 10, 20, 30 дней)"""
    try:
        # Получаем язык пользователя
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.tg_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                logger.error(f"❌ Пользователь {user_id} не найден для напоминания")
                return
            
            language = user.language
            
            # Если day = -1, это напоминание через 1 минуту (для всех языков)
            if day == -1:
                time_text = get_time_text(language, "1m")
                text = get_text(language, "regular_reminder", days_passed=time_text)
                await bot.send_message(chat_id=user_id, text=text)
                logger.info(f"✅ Напоминание через 1 минуту отправлено пользователю {user_id} (язык: {language})")
                
                # Записываем в activity и отмечаем в users
                from database_manager import DatabaseManager
                db_manager = DatabaseManager()
                await db_manager.log_reminder_sent(user_id, -1)
                await db_manager.mark_reminder_sent(user_id, "1m")
            # Если day = 0, это напоминание через 5 часов (для всех языков)
            elif day == 0:
                time_text = get_time_text(language, "5h")
                text = get_text(language, "regular_reminder", days_passed=time_text)
                await bot.send_message(chat_id=user_id, text=text)
                logger.info(f"✅ Напоминание через 5 часов отправлено пользователю {user_id} (язык: {language})")
                
                # Записываем в activity и отмечаем в users
                from database_manager import DatabaseManager
                db_manager = DatabaseManager()
                await db_manager.log_reminder_sent(user_id, 0)
                await db_manager.mark_reminder_sent(user_id, "5h")
            else:
                # Для дней (10, 20, 30)
                time_text = get_time_text(language, f"{day}d")
                text = get_text(language, "regular_reminder", days_passed=time_text)
                await bot.send_message(chat_id=user_id, text=text)
                logger.info(f"✅ Напоминание {day} дней отправлено пользователю {user_id} на языке {language}")
                
                # Записываем в activity и отмечаем в users
                from database_manager import DatabaseManager
                db_manager = DatabaseManager()
                await db_manager.log_reminder_sent(user_id, day)
                await db_manager.mark_reminder_sent(user_id, f"{day}d")
            
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")

async def send_final_reminder(user_id: int):
    """Отправляет финальное напоминание на 30-й день"""
    try:
        # Получаем язык пользователя
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.tg_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                logger.error(f"❌ Пользователь {user_id} не найден для финального напоминания")
                return
            
            language = user.language
            text = get_text(language, "final_reminder")
            
            await bot.send_message(chat_id=user_id, text=text)
            logger.info(f"✅ Финальное напоминание отправлено пользователю {user_id} на языке {language}")
            
            # Записываем в activity и отмечаем в users
            from database_manager import DatabaseManager
            db_manager = DatabaseManager()
            await db_manager.log_reminder_sent(user_id, 30)
            await db_manager.mark_reminder_sent(user_id, "30d")
            
    except Exception as e:
        logger.error(f"Ошибка при отправке финального напоминания пользователю {user_id}: {e}")

async def block_user_final(user_id: int):
    """Блокирует пользователя на 31-й день"""
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.tg_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                logger.error(f"❌ Пользователь {user_id} не найден для блокировки")
                return

            user.blocked = True
            await session.commit()

            # Отправляем сообщение о блокировке
            language = user.language
            text = get_text(language, "bot_liquidation_message")
            
            await bot.send_message(chat_id=user_id, text=text)
            logger.info(f"🚫 Пользователь {user_id} заблокирован на 31-й день")
            
            # Записываем в activity
            from database_manager import DatabaseManager
            db_manager = DatabaseManager()
            await db_manager.log_reminder_sent(user_id, 31)
            
    except Exception as e:
        logger.error(f"Ошибка при блокировке пользователя {user_id}: {e}")

# ====== 🧪 ТЕСТОВЫЕ ФУНКЦИИ ======

async def send_test_reminder(user_id: int, day: int):
    """Отправляет тестовое напоминание"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"📅 (ТЕСТ) Напоминание: прошло {day} дней"
        )
        logger.info(f"✅ Тестовое напоминание {day} дней отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")

async def block_test_user(user_id: int):
    """Тестовая блокировка пользователя через 31 день"""
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.tg_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            # Создаем пользователя для теста, если его нет
            user = User(
                tg_id=user_id,
                username=None,
                language="ru",
                blocked=False
            )
            session.add(user)
            await session.commit()
            logger.info(f"✅ Создан тестовый пользователь {user_id}")

        user.blocked = True
        await session.commit()

    try:
        await bot.send_message(
            chat_id=user_id,
            text="⛔️ (ТЕСТ) Срок взаимодействия истёк. Доступ к боту закрыт."
        )
        logger.info(f"🚫 Пользователь {user_id} заблокирован в тестовом режиме")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о блокировке пользователю {user_id}: {e}")

def setup_scheduler(bot_instance):
    global bot, scheduler
    bot = bot_instance
    scheduler = AsyncIOScheduler(timezone=TZ)
    scheduler.add_job(
        check_reminders,
        trigger="cron",
        hour=DAILY_REMINDER_HOUR,
        minute=DAILY_REMINDER_MINUTE,
        args=[bot],
        id="daily_reminders",
        replace_existing=True
    )
    scheduler.add_job(
        cleanup_users_after_31_days,
        trigger="cron",
        hour=23,
        minute=0,
        args=[bot],
        id="cleanup_31",
        replace_existing=True
    )
    scheduler.start()
    logger.info("📅 Планировщик напоминаний запущен")
    return scheduler