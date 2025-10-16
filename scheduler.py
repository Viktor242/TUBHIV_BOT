#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Планировщик напоминаний и финальных уведомлений"""

import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from database import async_session_maker, Case, User, Activity
from texts import get_text

TZ = pytz.timezone("Asia/Vladivostok")
DAILY_REMINDER_HOUR = 9
DAILY_REMINDER_MINUTE = 30

logger = logging.getLogger(__name__)


async def check_reminders(bot):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Case, User)
            .join(User, Case.user_id == User.id)
            .where(Case.active == True)
        )
        data = result.all()
        now = datetime.now(TZ)

        for case, user in data:
            reg = case.registered_at.replace(tzinfo=TZ)
            days_passed = (now.date() - reg.date()).days
            reminder_days = [5, 10, 15, 20, 25, 30]

            for rd in reminder_days:
                if days_passed >= rd and case.last_reminder_day < rd:
                    try:
                        deadline = case.deadline_at.strftime("%d.%m.%Y")
                        registered = reg.strftime("%d.%m.%Y")
                        remaining = max(0, 30 - days_passed)

                        if rd < 30:
                            text = (
                                f"⏰ Напоминание о дообследовании\n\n"
                                f"Дата регистрации: {registered}\n"
                                f"Прошло дней: {days_passed}\n"
                                f"Осталось дней: {remaining}\n"
                                f"Дата окончания: {deadline}\n\n"
                                f"Не забудьте пройти обследование вовремя!"
                            )
                            reminder_type = "regular"
                        else:
                            text = get_text(user.language, "final_reminder")
                            reminder_type = "final"
                            case.active = False

                        await bot.send_message(user.tg_id, text)
                        case.last_reminder_day = rd

                        activity = Activity(
                            user_id=user.id,
                            action_type="reminder_sent",
                            reminder_day=rd,
                            reminder_type=reminder_type,
                            is_final_reminder=(rd == 30),
                            reminder_date=now,
                            message_text=text
                        )
                        session.add(activity)
                        await session.commit()
                        logger.info(f"✅ Напоминание {rd}-й день для {user.tg_id}")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке уведомления {user.tg_id}: {e}")
                    break


async def cleanup_users_after_31_days(bot):
    async with async_session_maker() as session:
        now = datetime.now(TZ)
        cutoff = now - timedelta(days=31)

        result = await session.execute(
            select(Case, User)
            .join(User, Case.user_id == User.id)
            .where(
                Case.active == False,
                Case.expired == False,
                Case.last_reminder_day == 30,
                Case.registered_at < cutoff
            )
        )

        for case, user in result.all():
            try:
                text = get_text(user.language, "bot_liquidation_message")
                await bot.send_message(user.tg_id, text)
                case.expired = True

                activity = Activity(
                    user_id=user.id,
                    action_type="bot_liquidated",
                    reminder_day=31,
                    reminder_type="liquidation",
                    is_final_reminder=True,
                    bot_deleted=True,
                    reminder_date=now,
                    message_text=text
                )
                session.add(activity)
                await session.commit()
                logger.info(f"🚫 Финальное сообщение пользователю {user.tg_id}")
            except Exception as e:
                logger.error(f"Ошибка при отправке финального уведомления {user.tg_id}: {e}")


def setup_scheduler(bot):
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
