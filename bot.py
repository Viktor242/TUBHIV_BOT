#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный файл Telegram-бота для мигрантов
Управляет диалогами, регистрацией и напоминаниями
"""

import os
import logging
import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select
from dotenv import load_dotenv

from database import init_db, async_session_maker, User, Case
from texts import (
    CONSENT_TEXT, CONSENT_BUTTON_TEXT, CATEGORY_SELECT_TEXT, RESULT_RECEIVED_TEXT, RESULT_RECEIVED_MESSAGE,
    BUTTONS, INFO_TEXTS, HELP_TEXT, STATUS_TEXT, NO_ACTIVE_CASE, CASE_STOPPED
)
from scheduler import setup_scheduler

load_dotenv()

# Настройки
BOT_TOKEN = os.getenv("BOT_TOKEN")
TZ = pytz.timezone(os.getenv("TZ", "Asia/Vladivostok"))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Функция для правильного склонения слова "день"
def get_day_word(count: int) -> str:
    """Возвращает правильное склонение слова 'день'"""
    if count == 1:
        return "день"
    elif count in [2, 3, 4]:
        return "дня"
    else:
        return "дней"

# Функция для формирования текста следующего напоминания
def get_next_reminder_text(days_passed: int, next_reminder: int) -> str:
    """Формирует понятный текст о следующем напоминании"""
    day_word = get_day_word(next_reminder)
    
    if days_passed < 5:
        return f"Следующее напоминание: на 5-й день (через {next_reminder} {day_word})"
    elif days_passed < 10:
        return f"Следующее напоминание: на 10-й день (через {next_reminder} {day_word})"
    elif days_passed < 15:
        return f"Следующее напоминание: на 15-й день (через {next_reminder} {day_word})"
    elif days_passed < 20:
        return f"Следующее напоминание: на 20-й день (через {next_reminder} {day_word})"
    elif days_passed < 25:
        return f"Следующее напоминание: на 25-й день (через {next_reminder} {day_word})"
    elif days_passed < 30:
        return f"Следующее напоминание: на 30-й день (через {next_reminder} {day_word}) - ФИНАЛЬНОЕ"
    else:
        return "Все напоминания отправлены. Обследование завершено."

# Универсальная функция для создания клавиатуры
async def get_keyboard_for_user(user_tg_id: int) -> ReplyKeyboardMarkup:
    """Создает клавиатуру в зависимости от статуса пользователя"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == user_tg_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Проверяем, есть ли активные обследования
            active_cases_result = await session.execute(
                select(Case).where(
                    Case.user_id == user.id,
                    Case.active == True
                )
            )
            active_cases = active_cases_result.scalars().all()
            
            if active_cases:
                # Если есть активное обследование, показываем кнопку "Результат получен"
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text=RESULT_RECEIVED_TEXT)],
                        [KeyboardButton(text="❓ Помощь")]
                    ],
                    resize_keyboard=True
                )
        
        # Если нет активных обследований или пользователь не найден
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❓ Помощь")]],
            resize_keyboard=True
        )


# Состояния для FSM (Finite State Machine)
class RegistrationStates(StatesGroup):
    waiting_for_consent = State()
    waiting_for_category = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    async with async_session_maker() as session:
        # Проверяем, есть ли пользователь в базе
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Создаём нового пользователя
            user = User(
                tg_id=message.from_user.id,
                username=message.from_user.username
            )
            session.add(user)
            await session.commit()
            logger.info(f"Новый пользователь зарегистрирован: {message.from_user.id}")
        else:
            # Пользователь уже есть - проверяем, есть ли у него активные дела
            active_cases_result = await session.execute(
                select(Case).where(
                    Case.user_id == user.id,
                    Case.active == True
                )
            )
            active_cases = active_cases_result.scalars().all()
            
            if active_cases:
                # У пользователя есть активные дела - показываем статус
                latest_case = active_cases[0]  # Берем первое (самое последнее по времени)
                
                # Вычисляем статистику
                now = datetime.now(TZ)
                registered_at = latest_case.registered_at.replace(tzinfo=TZ) if latest_case.registered_at.tzinfo is None else latest_case.registered_at
                deadline_at = latest_case.deadline_at.replace(tzinfo=TZ) if latest_case.deadline_at.tzinfo is None else latest_case.deadline_at
                
                # Считаем дни с округлением в большую сторону
                total_seconds = (now - registered_at).total_seconds()
                days_passed = max(0, int(total_seconds // 86400) + (1 if total_seconds % 86400 > 0 else 0))
                days_remaining = max(0, (deadline_at - now).days)
                
                # Определяем следующее напоминание
                reminder_days = [5, 10, 15, 20, 25, 30]
                next_reminder = None
                for day in reminder_days:
                    if day > latest_case.last_reminder_day:
                        next_reminder = day - days_passed
                        break
                
                if next_reminder is None or next_reminder < 0:
                    next_reminder = 0
                
                # Форматируем даты
                registered_str = registered_at.strftime("%d.%m.%Y %H:%M")
                deadline_str = deadline_at.strftime("%d.%m.%Y")
                
                next_reminder_text = get_next_reminder_text(days_passed, next_reminder)
                status_message = STATUS_TEXT.format(
                    category=latest_case.category,
                    registered_at=registered_str,
                    days_passed=days_passed,
                    days_remaining=days_remaining,
                    deadline_at=deadline_str,
                    next_reminder_text=next_reminder_text
                )
                
                # Добавляем кнопки с результатом и помощью
                keyboard = await get_keyboard_for_user(message.from_user.id)
                await message.answer(status_message, reply_markup=keyboard)
                return
            else:
                # Нет активных дел - проверяем, есть ли остановленные (но не завершенные)
                stopped_cases_result = await session.execute(
                    select(Case).where(
                        Case.user_id == user.id,
                        Case.active == False,
                        Case.completed == False  # Только остановленные, не завершенные
                    ).order_by(Case.registered_at.desc())
                )
                stopped_cases = stopped_cases_result.scalars().all()
                
                if stopped_cases:
                    # Есть остановленные дела - возобновляем последнее
                    latest_case = stopped_cases[0]
                    latest_case.active = True
                    await session.commit()
                    
                    logger.info(f"Автоматически возобновлено обследование для пользователя {user.tg_id}")
                    
                    # Вычисляем статистику
                    now = datetime.now(TZ)
                    registered_at = latest_case.registered_at.replace(tzinfo=TZ) if latest_case.registered_at.tzinfo is None else latest_case.registered_at
                    deadline_at = latest_case.deadline_at.replace(tzinfo=TZ) if latest_case.deadline_at.tzinfo is None else latest_case.deadline_at
                    
                    # Считаем дни с округлением в большую сторону
                    total_seconds = (now - registered_at).total_seconds()
                    days_passed = max(0, int(total_seconds // 86400) + (1 if total_seconds % 86400 > 0 else 0))
                    days_remaining = max(0, (deadline_at - now).days)
                    
                    # Определяем следующее напоминание
                    reminder_days = [5, 10, 15, 20, 25, 30]
                    next_reminder = None
                    for day in reminder_days:
                        if day > latest_case.last_reminder_day:
                            next_reminder = day - days_passed
                            break
                    
                    if next_reminder is None or next_reminder < 0:
                        next_reminder = 0
                    
                    # Форматируем даты
                    registered_str = registered_at.strftime("%d.%m.%Y %H:%M")
                    deadline_str = deadline_at.strftime("%d.%m.%Y")
                    
                    next_reminder_text = get_next_reminder_text(days_passed, next_reminder)
                    status_message = f"✅ Напоминания возобновлены!\n\n{STATUS_TEXT.format(category=latest_case.category, registered_at=registered_str, days_passed=days_passed, days_remaining=days_remaining, deadline_at=deadline_str, next_reminder_text=next_reminder_text)}"
                    
                    # Добавляем кнопки с результатом и помощью
                    keyboard = await get_keyboard_for_user(message.from_user.id)
                    await message.answer(status_message, reply_markup=keyboard)
                    return
    
    # Создаём кнопку согласия
    consent_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=CONSENT_BUTTON_TEXT)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Отправляем согласие на обработку данных
    await message.answer(CONSENT_TEXT, reply_markup=consent_kb)
    await state.set_state(RegistrationStates.waiting_for_consent)


@dp.message(RegistrationStates.waiting_for_consent, F.text == CONSENT_BUTTON_TEXT)
async def process_consent(message: types.Message, state: FSMContext):
    """Обработка согласия на обработку данных"""
    # Создаём клавиатуру с категориями
    categories_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTONS["Туберкулез"])],
            [KeyboardButton(text=BUTTONS["Сифилис"])],
            [KeyboardButton(text=BUTTONS["ВИЧ-инфекция"])],
            [KeyboardButton(text=BUTTONS["Наркомания"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        CATEGORY_SELECT_TEXT,
        reply_markup=categories_kb
    )
    await state.set_state(RegistrationStates.waiting_for_category)


@dp.message(RegistrationStates.waiting_for_category)
async def process_category(message: types.Message, state: FSMContext):
    """Обработка выбора категории диагноза"""
    # Определяем категорию по тексту кнопки
    category = None
    for key, value in BUTTONS.items():
        if message.text == value:
            category = key
            break
    
    if not category:
        await message.answer("Пожалуйста, выбери категорию из предложенных кнопок.")
        return
    
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("Произошла ошибка. Пожалуйста, нажми /start заново.")
            await state.clear()
            return
        
        # Деактивируем старые активные обследования этой категории
        old_cases_result = await session.execute(
            select(Case).where(
                Case.user_id == user.id,
                Case.category == category,
                Case.active == True
            )
        )
        old_cases = old_cases_result.scalars().all()
        for old_case in old_cases:
            old_case.active = False
        
        # Создаём новое обследование
        now = datetime.now(TZ)
        deadline = now + timedelta(days=30)
        
        new_case = Case(
            user_id=user.id,
            category=category,
            registered_at=now,
            deadline_at=deadline,
            last_reminder_day=0,
            active=True
        )
        session.add(new_case)
        await session.commit()
        
        logger.info(f"Создано новое обследование для пользователя {user.tg_id}: {category}")
    
    # Отправляем информацию о диагнозе
    await message.answer(INFO_TEXTS[category], reply_markup=ReplyKeyboardRemove())
    
    # Создаём кнопки с результатом и помощью
    result_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=RESULT_RECEIVED_TEXT)],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "✅ Отлично! Я запомнил твой выбор и буду напоминать тебе каждые 5 дней.\n\n"
        "Если получишь результат раньше времени, нажми кнопку ниже.\n\n"
        "Используй команды:\n"
        "/status - узнать статус обследования\n"
        "/stop - остановить напоминания\n"
        "/help - справка",
        reply_markup=result_kb
    )
    
    await state.clear()


@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    """Показать статус обследования"""
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer(NO_ACTIVE_CASE)
            return
        
        # Получаем активное обследование (берем самое последнее)
        case_result = await session.execute(
            select(Case).where(
                Case.user_id == user.id,
                Case.active == True
            ).order_by(Case.registered_at.desc()).limit(1)
        )
        case = case_result.scalar_one_or_none()
        
        if not case:
            await message.answer(NO_ACTIVE_CASE)
            return
        
        # Вычисляем статистику
        now = datetime.now(TZ)
        registered_at = case.registered_at.replace(tzinfo=TZ) if case.registered_at.tzinfo is None else case.registered_at
        deadline_at = case.deadline_at.replace(tzinfo=TZ) if case.deadline_at.tzinfo is None else case.deadline_at
        
        # Считаем дни с округлением в большую сторону
        total_seconds = (now - registered_at).total_seconds()
        days_passed = max(0, int(total_seconds // 86400) + (1 if total_seconds % 86400 > 0 else 0))
        days_remaining = max(0, (deadline_at - now).days)
        
        # Определяем следующее напоминание
        reminder_days = [5, 10, 15, 20, 25, 30]
        next_reminder = None
        for day in reminder_days:
            if day > case.last_reminder_day:
                next_reminder = day - days_passed
                break
        
        if next_reminder is None or next_reminder < 0:
            next_reminder = 0
        
        # Форматируем даты
        registered_str = registered_at.strftime("%d.%m.%Y %H:%M")
        deadline_str = deadline_at.strftime("%d.%m.%Y")
        
        next_reminder_text = get_next_reminder_text(days_passed, next_reminder)
        status_message = STATUS_TEXT.format(
            category=case.category,
            registered_at=registered_str,
            days_passed=days_passed,
            days_remaining=days_remaining,
            deadline_at=deadline_str,
            next_reminder_text=next_reminder_text
        )
        
    # Добавляем кнопки с результатом и помощью
    keyboard = await get_keyboard_for_user(message.from_user.id)
    await message.answer(status_message, reply_markup=keyboard)


@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    """Остановить напоминания"""
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer(NO_ACTIVE_CASE)
            return
        
        # Деактивируем все активные обследования
        cases_result = await session.execute(
            select(Case).where(
                Case.user_id == user.id,
                Case.active == True
            )
        )
        cases = cases_result.scalars().all()
        
        if not cases:
            await message.answer(NO_ACTIVE_CASE)
            return
        
        for case in cases:
            case.active = False
        
        await session.commit()
        
        logger.info(f"Остановлены напоминания для пользователя {user.tg_id}")
    
    # Добавляем кнопку помощи
    keyboard = await get_keyboard_for_user(message.from_user.id)
    await message.answer(CASE_STOPPED, reply_markup=keyboard)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Показать справку"""
    keyboard = await get_keyboard_for_user(message.from_user.id)
    await message.answer(HELP_TEXT, reply_markup=keyboard)


@dp.message(F.text == RESULT_RECEIVED_TEXT)
async def btn_result_received(message: types.Message, state: FSMContext):
    """Обработка кнопки Результат получен"""
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("Произошла ошибка. Пожалуйста, нажми /start заново.")
            return
        
        # Деактивируем все активные обследования
        cases_result = await session.execute(
            select(Case).where(
                Case.user_id == user.id,
                Case.active == True
            )
        )
        cases = cases_result.scalars().all()
        
        if not cases:
            await message.answer("У тебя нет активных обследований.")
            return
        
        for case in cases:
            case.active = False
            case.completed = True  # Помечаем как завершенное пользователем
        
        await session.commit()
        
        logger.info(f"Результат получен для пользователя {user.tg_id}")
    
    # Создаём клавиатуру с категориями для нового обследования
    categories_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTONS["Туберкулез"])],
            [KeyboardButton(text=BUTTONS["Сифилис"])],
            [KeyboardButton(text=BUTTONS["ВИЧ-инфекция"])],
            [KeyboardButton(text=BUTTONS["Наркомания"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        RESULT_RECEIVED_MESSAGE,
        reply_markup=categories_kb
    )
    
    # Устанавливаем состояние для выбора категории
    await state.set_state(RegistrationStates.waiting_for_category)


@dp.message(F.text == "❓ Помощь")
async def btn_help(message: types.Message):
    """Обработка кнопки Помощь"""
    keyboard = await get_keyboard_for_user(message.from_user.id)
    await message.answer(HELP_TEXT, reply_markup=keyboard)


async def main():
    """Главная функция запуска бота"""
    # Инициализируем базу данных
    await init_db()
    logger.info("База данных инициализирована")
    
    # Настраиваем планировщик
    scheduler = setup_scheduler(bot)
    
    try:
        # Запускаем бота
        logger.info("Бот запущен")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        # Останавливаем планировщик при завершении
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

