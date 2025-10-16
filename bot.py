#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный файл Telegram-бота для мигрантов
Управляет диалогами, регистрацией и напоминаниями
"""

# from keep_alive import keep_alive
# keep_alive()

import os
import logging
import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from sqlalchemy.exc import IntegrityError
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeChat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select
from dotenv import load_dotenv

from database import init_db, async_session_maker, User, Case, Activity
from texts import (
    CONSENT_TEXT, CONSENT_BUTTON_TEXT, CATEGORY_SELECT_TEXT, RESULT_RECEIVED_TEXT, RESULT_RECEIVED_MESSAGE,
    BUTTONS, INFO_TEXTS, HELP_TEXT, STATUS_TEXT, NO_ACTIVE_CASE, CASE_STOPPED, get_text, TEXTS
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

# Функция для логирования действий пользователя
async def log_user_action(user_id: int, action_type: str, action_data: str = None, message_text: str = None):
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
                
                # Создаем запись о действии
                action = Activity(
                    user_id=user.id,
                    action_type=russian_action_type,
                    action_data=russian_action_data,
                    message_text=message_text
                )
                session.add(action)
                await session.commit()
                
                logger.info(f"📝 Действие записано: User {user_id} | {russian_action_type} | {russian_action_data}")
            else:
                logger.warning(f"⚠️ Пользователь {user_id} не найден для логирования действия {action_type}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при логировании действия пользователя {user_id}: {e}")

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Функция для правильного склонения слова "день"
def get_day_word(count: int, language: str = "ru") -> str:
    """Возвращает правильное склонение слова 'день'"""
    if language == "ru":
        if count == 1:
            return "день"
        elif count in [2, 3, 4]:
            return "дня"
        else:
            return "дней"
    elif language == "uz":
        return "kun"
    elif language == "zh":
        return "天"
    elif language == "ko":
        return "일"
    elif language == "en":
        return "day" if count == 1 else "days"
    else:
        return "день"

# Функция для формирования текста следующего напоминания
def get_next_reminder_text(days_passed: int, next_reminder: int, language: str = "ru") -> str:
    """Формирует понятный текст о следующем напоминании"""
    day_word = get_day_word(next_reminder, language)
    
    if days_passed < 5:
        return get_text(language, "next_reminder_5").format(next_reminder=next_reminder, day_word=day_word)
    elif days_passed < 10:
        return get_text(language, "next_reminder_10").format(next_reminder=next_reminder, day_word=day_word)
    elif days_passed < 15:
        return get_text(language, "next_reminder_15").format(next_reminder=next_reminder, day_word=day_word)
    elif days_passed < 20:
        return get_text(language, "next_reminder_20").format(next_reminder=next_reminder, day_word=day_word)
    elif days_passed < 25:
        return get_text(language, "next_reminder_25").format(next_reminder=next_reminder, day_word=day_word)
    elif days_passed < 30:
        return get_text(language, "next_reminder_30").format(next_reminder=next_reminder, day_word=day_word)
    else:
        return get_text(language, "all_reminders_sent")

# Функция для создания inline клавиатуры выбора языка
def get_language_keyboard() -> InlineKeyboardMarkup:
    """Создает inline клавиатуру для выбора языка"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")
            ],
            [
                InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_zh"),
                InlineKeyboardButton(text="🇰🇷 한국어", callback_data="lang_ko")
            ],
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
            ]
        ]
    )

# Функция для создания inline клавиатуры выбора диагноза
def get_diagnosis_keyboard(language: str) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру для выбора диагноза"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(language, "tuberculosis"), callback_data="diag_tuberculosis"),
                InlineKeyboardButton(text=get_text(language, "syphilis"), callback_data="diag_syphilis")
            ],
            [
                InlineKeyboardButton(text=get_text(language, "hiv"), callback_data="diag_hiv"),
                InlineKeyboardButton(text=get_text(language, "drug_addiction"), callback_data="diag_drug_addiction")
            ]
        ]
    )

# Функция для создания inline клавиатуры действий после выбора диагноза
def get_diagnosis_actions_keyboard(language: str) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру действий после выбора диагноза"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(language, "show_documents"), callback_data="show_documents"),
                InlineKeyboardButton(text=get_text(language, "understood_10_days"), callback_data="understood_10_days")
            ]
        ]
    )

# Функция для создания inline клавиатуры результата обследования
def get_examination_result_keyboard(language: str) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру результата обследования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(language, "passed_examination"), callback_data="passed_examination"),
                InlineKeyboardButton(text=get_text(language, "not_passed_examination"), callback_data="not_passed_examination")
            ]
        ]
    )

# Универсальная функция для создания клавиатуры
async def get_keyboard_for_user(user_tg_id: int) -> ReplyKeyboardMarkup:
    """Создает клавиатуру в зависимости от статуса пользователя"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == user_tg_id)
        )
        user = result.scalar_one_or_none()
        
        language = user.language if user else "ru"
        
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=get_text(language, "start_button"))],
                [KeyboardButton(text=get_text(language, "status_button")), KeyboardButton(text=get_text(language, "help_button"))]
            ],
            resize_keyboard=True
        )


# Состояния для FSM (Finite State Machine)
class RegistrationStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_consent = State()
    waiting_for_category = State()

class DiagnosisStates(StatesGroup):
    waiting_for_understanding = State()  # Ждем "Я понял"
    waiting_for_result = State()         # Ждем "Прошел/Не прошел"


@dp.message(CommandStart())
async def cmd_start_handler(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    await cmd_start(message, state)


async def show_language_selection(message: types.Message, state: FSMContext):
    """Показать выбор языка"""
    user_id = message.from_user.id
    username = message.from_user.username or "Без имени"
    
    # Логируем регистрацию
    logger.info(f"🆔 ID: {user_id} | Пользователь: {username} | Зарегистрировался")
    
    # Логируем действие в БД
    await log_user_action(user_id, "bot_started", None, f"Username: {username}")
    
    async with async_session_maker() as session:
        # Проверяем, есть ли пользователь в базе
        result = await session.execute(
            select(User).where(User.tg_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        is_new_user = False  # Флаг для определения нового пользователя
        
        if not user:
            # Создаём нового пользователя
            try:
                user = User(
                    tg_id=user_id,
                    username=username
                )
                session.add(user)
                await session.commit()
                is_new_user = True
                logger.info(f"✅ Новый пользователь зарегистрирован: ID {user_id} | {username}")
            except IntegrityError:
                # Пользователь уже существует - откатываем транзакцию
                await session.rollback()
                logger.info(f"⚠️ Пользователь {user_id} уже есть в базе")
                is_new_user = False  # Устанавливаем флаг для существующего пользователя
                # Получаем существующего пользователя
                result = await session.execute(
                    select(User).where(User.tg_id == user_id)
                )
                user = result.scalar_one_or_none()
        else:
            logger.info(f"🔄 Существующий пользователь: ID {user_id} | {username}")
            is_new_user = False  # Устанавливаем флаг для существующего пользователя
            
            # Проверяем, есть ли активные дела
            active_cases_result = await session.execute(
                select(Case).where(
                    Case.user_id == user.id,
                    Case.active == True
                )
            )
            active_cases = active_cases_result.scalars().all()
            
            if active_cases:
                # У пользователя есть активные дела - показываем статус
                latest_case = active_cases[0]
                
                # Вычисляем статистику
                now = datetime.now(TZ)
                registered_at = latest_case.registered_at.replace(tzinfo=TZ) if latest_case.registered_at.tzinfo is None else latest_case.registered_at
                deadline_at = latest_case.deadline_at.replace(tzinfo=TZ) if latest_case.deadline_at.tzinfo is None else latest_case.deadline_at
                
                # Считаем календарные дни
                registration_date = registered_at.date()
                current_date = now.date()
                days_passed = max(0, (current_date - registration_date).days)
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
                
                next_reminder_text = get_next_reminder_text(days_passed, next_reminder, user.language)
                status_message = get_text(user.language, "status_text",
                    category=latest_case.category,
                    registered_at=registered_str,
                    days_passed=days_passed,
                    days_remaining=days_remaining,
                    deadline_at=deadline_str,
                    next_reminder_text=next_reminder_text
                )
                
                # Добавляем кнопки с результатом и помощью
                keyboard = await get_keyboard_for_user(user_id)
                await message.answer(status_message, reply_markup=keyboard)
                return
            else:
                # Нет активных дел - проверяем, есть ли остановленные (но не завершенные)
                stopped_cases_result = await session.execute(
                    select(Case).where(
                        Case.user_id == user.id,
                        Case.active == False,
                        Case.completed == False
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
                    
                    # Считаем календарные дни
                    registration_date = registered_at.date()
                    current_date = now.date()
                    days_passed = max(0, (current_date - registration_date).days)
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
                    
                    next_reminder_text = get_next_reminder_text(days_passed, next_reminder, user.language)
                    status_message = f"✅ Напоминания возобновлены!\n\n{get_text(user.language, 'status_text', category=latest_case.category, registered_at=registered_str, days_passed=days_passed, days_remaining=days_remaining, deadline_at=deadline_str, next_reminder_text=next_reminder_text)}"
                    
                    # Добавляем кнопки с результатом и помощью
                    keyboard = await get_keyboard_for_user(user_id)
                    await message.answer(status_message, reply_markup=keyboard)
                    return
    
    # Если пользователь новый или нет активных дел - показываем выбор языка
    language_kb = get_language_keyboard()
    
    # Определяем, новый пользователь или уже зарегистрированный
    if is_new_user:
        # Новый пользователь - используем дефолтный язык для сообщения
        registration_status = get_text("ru", "registered_new")
    else:
        # Пользователь уже зарегистрирован - используем дефолтный язык для сообщения
        registration_status = get_text("ru", "registered_existing")
    
    await message.answer(
        f"{get_text('ru', 'your_id', user_id=user_id)}\n{registration_status}\n\n{get_text('ru', 'language_select')}", 
        reply_markup=language_kb
    )
    await state.set_state(RegistrationStates.waiting_for_language)


async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start с проверкой состояния"""
    # Получаем текущее состояние пользователя
    current_state = await state.get_state()
    
    # Если пользователь находится в любом процессе, сбрасываем его
    if current_state in [
        RegistrationStates.waiting_for_language,
        RegistrationStates.waiting_for_consent,
        RegistrationStates.waiting_for_category,
        DiagnosisStates.waiting_for_understanding,
        DiagnosisStates.waiting_for_result
    ]:
        # Очищаем состояние
        await state.clear()
        # Возвращаем к выбору языка
        await show_language_selection(message, state)
        return
    
    # Если состояние пустое, показываем выбор языка
    await show_language_selection(message, state)


# Обработчик выбора языка
@dp.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора языка"""
    language = callback.data.split("_")[1]  # ru, uz, zh, ko, en
    
    # Логируем выбор языка
    await log_user_action(callback.from_user.id, "language_selected", language)
    
    async with async_session_maker() as session:
        # Обновляем язык пользователя
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.language = language
            await session.commit()
            logger.info(f"Пользователь {callback.from_user.id} выбрал язык: {language}")
            
            # Обновляем команды для пользователя
            await update_user_commands(callback.from_user.id, language)
    
    # Показываем важное сообщение сразу после выбора языка
    important_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(language, "understood_month"), callback_data="understood_month")]
        ]
    )
    
    await callback.message.edit_text(
        get_text(language, "important_message"),
        reply_markup=important_kb
    )
    await state.set_state(RegistrationStates.waiting_for_consent)


# Обработчик "Я понял про месяц"
@dp.callback_query(F.data == "understood_month")
async def process_understood_month(callback: types.CallbackQuery, state: FSMContext):
    """Обработка понимания про месяц"""
    # Логируем действие
    await log_user_action(callback.from_user.id, "button_pressed", "understood_month")
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    # Показываем выбор диагноза
    diagnosis_kb = get_diagnosis_keyboard(language)
    await callback.message.edit_text(
        get_text(language, "diagnosis_found"),
        reply_markup=diagnosis_kb
    )
    await state.set_state(RegistrationStates.waiting_for_category)


# Обработчик выбора диагноза
@dp.callback_query(F.data.startswith("diag_"))
async def process_diagnosis_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора диагноза"""
    diagnosis = callback.data.split("_", 1)[1]  # tuberculosis, syphilis, hiv, drug_addiction
    
    # Логируем выбор диагноза
    await log_user_action(callback.from_user.id, "diagnosis_chosen", diagnosis)
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    # Показываем информацию о диагнозе
    diagnosis_info = get_text(language, f"{diagnosis}_info")
    actions_kb = get_diagnosis_actions_keyboard(language)
    
    await callback.message.edit_text(
        diagnosis_info,
        reply_markup=actions_kb
    )
    await state.set_state(DiagnosisStates.waiting_for_understanding)


# Обработчик "Показать документы"
@dp.callback_query(F.data == "show_documents")
async def process_show_documents(callback: types.CallbackQuery, state: FSMContext):
    """Показать список документов"""
    # Логируем действие
    await log_user_action(callback.from_user.id, "button_pressed", "show_documents")
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    await callback.answer(get_text(language, "documents_reminder"), show_alert=True)


# Обработчик "Я понял про 10 дней"
@dp.callback_query(F.data == "understood_10_days")
async def process_understood_10_days(callback: types.CallbackQuery, state: FSMContext):
    """Обработка понимания про 10 дней"""
    # Логируем действие
    await log_user_action(callback.from_user.id, "button_pressed", "understood_10_days")
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    # Показываем кнопки результата обследования
    result_kb = get_examination_result_keyboard(language)
    await callback.message.edit_text(
        get_text(language, "understood_10_days_examination"),
        reply_markup=result_kb
    )
    await state.set_state(DiagnosisStates.waiting_for_result)


# Обработчик "Я прошел дообследования"
@dp.callback_query(F.data == "passed_examination")
async def process_passed_examination(callback: types.CallbackQuery, state: FSMContext):
    """Обработка прохождения обследования"""
    # Логируем действие
    await log_user_action(callback.from_user.id, "button_pressed", "passed_examination")
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    # Показываем сообщение о справке в Лотос
    await callback.message.edit_text(
        get_text(language, "waiting_certificate")
    )
    await state.clear()


# Обработчик "Я не прошел дообследование"
@dp.callback_query(F.data == "not_passed_examination")
async def process_not_passed_examination(callback: types.CallbackQuery, state: FSMContext):
    """Обработка непрохождения обследования"""
    # Логируем действие
    await log_user_action(callback.from_user.id, "button_pressed", "not_passed_examination")
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        language = user.language if user else "ru"
    
    # Возвращаемся к выбору диагноза
    diagnosis_kb = get_diagnosis_keyboard(language)
    await callback.message.edit_text(
        get_text(language, "diagnosis_found"),
        reply_markup=diagnosis_kb
    )
    await state.set_state(RegistrationStates.waiting_for_category)


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
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("Ошибка: пользователь не найден")
            return
        
        # Определяем категорию по тексту кнопки
        category = None
        for key, value in BUTTONS.items():
            if message.text == value:
                category = key
                break
        
        if not category:
            await message.answer(get_text(user.language, "choose_category"))
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
        # Срок 30 дней с момента регистрации пользователя в боте
        user_created_at = user.created_at.replace(tzinfo=TZ) if user.created_at.tzinfo is None else user.created_at
        deadline = user_created_at + timedelta(days=30)
        
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
            [KeyboardButton(text=get_text(user.language, "result_received"))],
            [KeyboardButton(text=get_text(user.language, "status_button")), KeyboardButton(text=get_text(user.language, "help_button"))]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        get_text(user.language, "result_received_message"),
        reply_markup=result_kb
    )
    
    await state.clear()


async def show_registration_status(message: types.Message, user):
    """Показать статус регистрации пользователя"""
    user_created_at = user.created_at.replace(tzinfo=TZ) if user.created_at.tzinfo is None else user.created_at
    user_registered_str = user_created_at.strftime("%d.%m.%Y %H:%M")
    
    now = datetime.now(TZ)
    # Считаем календарные дни (если зарегистрировался 16.10, то 16.10 = 0 дней, 17.10 = 1 день)
    registration_date = user_created_at.date()
    current_date = now.date()
    days_since_registration = (current_date - registration_date).days
    
    # Создаем сообщение напрямую без использования get_text
    if user.language == "ru":
        status_text = (
            "📊 СТАТУС РЕГИСТРАЦИИ\n\n"
            f"🆔 Ваш ID: {user.tg_id}\n"
            f"Дата регистрации: {user_registered_str}\n"
            f"Прошло дней с регистрации: {days_since_registration}"
        )
    elif user.language == "uz":
        status_text = (
            "📊 RO'YXATDAN O'TISH HOLATI\n\n"
            f"🆔 Sizning ID: {user.tg_id}\n"
            f"Ro'yxatdan o'tish sanasi: {user_registered_str}\n"
            f"Ro'yxatdan o'tishdan beri kunlar: {days_since_registration}"
        )
    elif user.language == "zh":
        status_text = (
            "📊 注册状态\n\n"
            f"🆔 您的ID: {user.tg_id}\n"
            f"注册日期: {user_registered_str}\n"
            f"注册后已过天数: {days_since_registration}"
        )
    elif user.language == "ko":
        status_text = (
            "📊 등록 상태\n\n"
            f"🆔 귀하의 ID: {user.tg_id}\n"
            f"등록 날짜: {user_registered_str}\n"
            f"등록 후 경과 일수: {days_since_registration}"
        )
    else:  # en
        status_text = (
            "📊 REGISTRATION STATUS\n\n"
            f"🆔 Your ID: {user.tg_id}\n"
            f"Registration date: {user_registered_str}\n"
            f"Days since registration: {days_since_registration}"
        )
    
    # Убираем клавиатуру полностью - показываем только текст Status
    await message.answer(status_text)


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
            # Если пользователь не найден, отправляем сообщение на русском (по умолчанию)
            await message.answer(get_text("ru", "no_active_case"))
            return
        
        # Получаем любое обследование (берем самое последнее, даже неактивное)
        case_result = await session.execute(
            select(Case).where(
                Case.user_id == user.id
            ).order_by(Case.registered_at.desc()).limit(1)
        )
        case = case_result.scalar_one_or_none()
        
        if not case:
            # Если нет обследований, показываем только регистрацию пользователя
            await show_registration_status(message, user)
            return
        
        # Проверяем, истек ли срок
        if case.expired:
            user_created_at = user.created_at.replace(tzinfo=TZ) if user.created_at.tzinfo is None else user.created_at
            user_registered_str = user_created_at.strftime("%d.%m.%Y %H:%M")
            expired_message = get_text(user.language, "expired_status").format(
                user_id=user.tg_id,
                category=case.category,
                registered_at=user_registered_str
            )
            # Убираем клавиатуру полностью - показываем только текст Status
            await message.answer(expired_message)
            return
        
        # Вычисляем статистику
        now = datetime.now(TZ)
        user_created_at = user.created_at.replace(tzinfo=TZ) if user.created_at.tzinfo is None else user.created_at
        case_registered_at = case.registered_at.replace(tzinfo=TZ) if case.registered_at.tzinfo is None else case.registered_at
        deadline_at = case.deadline_at.replace(tzinfo=TZ) if case.deadline_at.tzinfo is None else case.deadline_at
        
        # Считаем календарные дни
        registration_date = user_created_at.date()
        current_date = now.date()
        days_passed = max(0, (current_date - registration_date).days)
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
        user_registered_str = user_created_at.strftime("%d.%m.%Y %H:%M")  # Дата первого посещения
        deadline_str = deadline_at.strftime("%d.%m.%Y")
        
        next_reminder_text = get_next_reminder_text(days_passed, next_reminder, user.language)
        status_message = get_text(user.language, "status_text").format(
            user_id=user.tg_id,
            category=case.category,
            registered_at=user_registered_str,  # Теперь показываем дату первого посещения
            days_passed=days_passed,
            days_remaining=days_remaining,
            deadline_at=deadline_str,
            next_reminder_text=next_reminder_text
        )
        
    # Убираем клавиатуру полностью - показываем только текст Status
    await message.answer(status_message)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Показать справку"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer(get_text("ru", "error_occurred"))
            return
            
        # Убираем клавиатуру полностью - показываем только текст Help
        await message.answer(get_text(user.language, "help_text"))


# Обработчики кнопок на разных языках
@dp.message(F.text.in_(["🚀 Старт", "🚀 Boshlash", "🚀 开始", "🚀 시작", "🚀 Start"]))
async def btn_start_multilang(message: types.Message, state: FSMContext):
    """Обработка кнопки Старт на всех языках"""
    await cmd_start(message, state)


@dp.message(F.text.in_(["📊 Статус", "📊 Holat", "📊 状态", "📊 상태", "📊 Status"]))
async def btn_status_multilang(message: types.Message):
    """Обработка кнопки Статус на всех языках"""
    await cmd_status(message)


@dp.message(F.text.in_(["❓ Помощь", "❓ Yordam", "❓ 帮助", "❓ 도움말", "❓ Help"]))
async def btn_help_multilang(message: types.Message):
    """Обработка кнопки Помощь на всех языках"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer(get_text("ru", "error_occurred"))
            return
            
        # Убираем клавиатуру полностью - показываем только текст Help
        await message.answer(get_text(user.language, "help_text"))


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
            await message.answer(get_text(user.language, "error_occurred"))
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
            await message.answer(get_text(user.language, "no_active_examinations"))
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


async def update_user_commands(user_id: int, language: str):
    """Обновляет команды для конкретного пользователя - только на английском языке"""
    # Всегда используем английские команды независимо от языка пользователя
    commands = [
        BotCommand(command="start", description="🚀 Open menu"),
        BotCommand(command="status", description="📊 Registration status"),
        BotCommand(command="help", description="❓ How does the bot work?")
    ]
    
    # Устанавливаем команды для конкретного пользователя
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))


async def setup_bot_commands():
    """Устанавливает команды бота только на английском языке"""
    commands = [
        BotCommand(command="start", description="🚀 Open menu"),
        BotCommand(command="status", description="📊 Registration status"),
        BotCommand(command="help", description="❓ How does the bot work?")
    ]
    
    # Сначала очищаем все команды
    await bot.set_my_commands([])
    
    # Затем устанавливаем команды только на английском языке
    await bot.set_my_commands(commands)


async def main():
    """Главная функция запуска бота"""
    # Инициализируем базу данных
    await init_db()
    logger.info("База данных инициализирована")
    
    # Настраиваем планировщик
    scheduler = setup_scheduler(bot)
    
    # Настраиваем команды бота
    await setup_bot_commands()
    
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

