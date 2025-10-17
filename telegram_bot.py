#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основной класс Telegram бота
"""

import logging
import asyncio
from datetime import datetime, timedelta
import threading
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from database import init_db
from database_manager import DatabaseManager
from button_handler import ButtonHandler
from texts import get_text, CONSENT_BUTTON_TEXT
from utils import get_language_keyboard, get_keyboard_for_user
from states import RegistrationStates, DiagnosisStates
from scheduler import setup_scheduler
import pytz

TZ = pytz.timezone("Asia/Vladivostok")

logger = logging.getLogger(__name__)

class TelegramBot:
    """Основной класс Telegram бота"""
    
    def __init__(self):
        load_dotenv()
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Инициализируем менеджеры
        self.db_manager = DatabaseManager()
        self.button_handler = ButtonHandler(self.db_manager, self.bot)
        
        # Регистрируем обработчики
        self._register_handlers()
    
    async def block_inactive_users(self, message: types.Message):
        """Блокирует заблокированных пользователей"""
        async with self.db_manager.session_maker() as session:
            from sqlalchemy import select
            from database import User
            
            result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
            user = result.scalar_one_or_none()
            if user and user.blocked:
                await message.answer("⛔️ Доступ к боту закрыт. Срок взаимодействия истёк.")
                return True  # блокируем дальнейшую обработку
        return False  # продолжаем обработку
    
    async def block_inactive_callbacks(self, callback: types.CallbackQuery):
        """Блокирует заблокированных пользователей для callback запросов"""
        async with self.db_manager.session_maker() as session:
            from sqlalchemy import select
            from database import User
            
            result = await session.execute(select(User).where(User.tg_id == callback.from_user.id))
            user = result.scalar_one_or_none()
            if user and user.blocked:
                await callback.answer("⛔️ Доступ к боту закрыт.", show_alert=True)
                return True  # блокируем дальнейшую обработку
        return False  # продолжаем обработку
    
    def _register_handlers(self):
        """Регистрирует все обработчики"""
        
        # Команды (с проверкой блокировки)
        self.dp.message(CommandStart())(self.cmd_start)
        self.dp.message(Command("status"))(self.cmd_status)
        self.dp.message(Command("help"))(self.cmd_help)
        self.dp.message(Command("test_cycle"))(self.cmd_test_cycle)  # ТЕСТОВАЯ КОМАНДА
        
        # Обработчики кнопок главного меню (для всех языков)
        
        # Inline handlers для выбора языка
        self.dp.callback_query.register(self.handle_language_callback, F.data.startswith("lang_"))
        
        # Inline handlers для кнопки "Понял"
        self.dp.callback_query.register(self.handle_understood_month_callback, F.data.startswith("understood_month_"))
        
        # Inline handlers для выбора диагноза
        self.dp.callback_query.register(self.handle_diagnosis_callback, F.data.startswith("diag_"))
        
        # Inline handlers для действий после выбора диагноза
        self.dp.callback_query.register(self.handle_show_documents_callback, F.data == "show_documents")
        self.dp.callback_query.register(self.handle_understood_examination_callback, F.data == "understood_examination")
        
        # Inline handlers для результатов обследования
        self.dp.callback_query.register(self.handle_passed_examination_callback, F.data == "passed_examination")
        self.dp.callback_query.register(self.handle_not_passed_examination_callback, F.data == "not_passed_examination")
        # Обработчики для кнопок Status и Help на всех языках
        for lang in ["ru", "uz", "zh", "ko", "en"]:
            self.dp.message.register(self.handle_status_button, F.text == get_text(lang, "status_button"))
            self.dp.message.register(self.handle_help_button, F.text == get_text(lang, "help_button"))
        
        # Обработчики для popup кнопок
        self.dp.callback_query.register(self.handle_status_popup, F.data == "show_status_popup")
        self.dp.callback_query.register(self.handle_help_popup, F.data == "show_help_popup")
        
        # Message handlers для текстовых кнопок (если остались)
        self.dp.message.register(self.handle_understood_month, F.text == get_text("ru", "understood_month"))
        self.dp.message.register(self.handle_understood_10_days, F.text == get_text("ru", "understood_10_days_examination"))
        self.dp.message.register(self.handle_understood_examination, F.text == get_text("ru", "understood_examination"))
        self.dp.message.register(self.handle_passed_examination, F.text == get_text("ru", "passed_examination"))
        self.dp.message.register(self.handle_not_passed_examination, F.text == get_text("ru", "not_passed_examination"))
        self.dp.message.register(self.handle_result_received, F.text == get_text("ru", "result_received"))
        self.dp.message.register(self.handle_show_documents, F.text == get_text("ru", "show_documents"))
        
        # Message handlers
        self.dp.message(RegistrationStates.waiting_for_language)(self.process_language_selection)
    
    # Callback handlers - обертки для ButtonHandler
    async def handle_language_selection(self, callback: types.CallbackQuery, state: FSMContext):
        await self.button_handler.process_language_selection(callback, state)
    
    async def handle_understood_month(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_understood_month(callback, state)
    
    async def handle_diagnosis_selection(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_diagnosis_selection(callback, state)
    
    async def handle_understood_10_days(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_understood_10_days(callback, state)
    
    async def handle_understood_examination(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_understood_examination(callback, state)
    
    async def handle_passed_examination(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_passed_examination(callback, state)
    
    async def handle_not_passed_examination(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_not_passed_examination(callback, state)
    
    async def handle_result_received(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_result_received(callback, state)
    
    async def handle_status_button(self, message: types.Message, state: FSMContext):
        await self.button_handler.process_status_button(message, state)
    
    async def handle_help_button(self, message: types.Message, state: FSMContext):
        await self.button_handler.process_help_button(message, state)
    
    async def handle_status_popup(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка popup для статуса"""
        user = await self.db_manager.get_user_by_tg_id(callback.from_user.id)
        if not user:
            await callback.answer(get_text("ru", "no_active_case"), show_alert=True)
            return
        
        # Получаем язык пользователя
        language = user.language
        
        # Простой статус без сложной логики
        from datetime import datetime, timedelta
        now = datetime.now()
        days_passed = (now - user.created_at).days
        days_remaining = max(0, 31 - days_passed)
        
        # Простое сообщение о статусе на языке пользователя
        status_text = (
            f"🆔 {get_text(language, 'user_id')}: {user.tg_id}\n"
            f"📅 {get_text(language, 'registration_date')}: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"✅ {get_text(language, 'already_registered')}\n"
            f"⏰ {get_text(language, 'days_left', days=days_remaining)}"
        )
        
        await callback.answer(status_text, show_alert=True)
    
    async def handle_help_popup(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка popup для справки"""
        user = await self.db_manager.get_user_by_tg_id(callback.from_user.id)
        language = user.language if user else "ru"
        
        await callback.answer(get_text(language, "help_text"), show_alert=True)
    
    async def handle_show_documents(self, message: types.Message, state: FSMContext):
        # Создаем временный callback для совместимости
        callback = types.CallbackQuery(
            id="temp",
            from_user=message.from_user,
            chat_instance="temp",
            message=message
        )
        await self.button_handler.process_show_documents(callback, state)
    
    # Основные команды
    async def cmd_start(self, message: types.Message, state: FSMContext):
        """Обработка команды /start — показ информации и меню с кнопками (Builder)"""
        # Проверяем блокировку
        if await self.block_inactive_users(message):
            return
            
        user_id = message.from_user.id
        
        # Создаем пользователя, если его нет
        user = await self.db_manager.get_user_by_tg_id(user_id)
        is_new_user = False
        if not user:
            user = await self.db_manager.create_user(
                tg_id=user_id,
                username=message.from_user.username
            )
            is_new_user = True
        
        # Получаем пользователя после создания
        user = await self.db_manager.get_user_by_tg_id(user_id)
        
        if user:
            registration_date = user.created_at.strftime("%d.%m.%Y %H:%M") if user.created_at else datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
            registration_status = "Вы зарегистрированы" if is_new_user else "Вы уже зарегистрированы"
            
            # Вычисляем реальное количество дней до дедлайна
            if user.deadline:
                now = datetime.now(TZ)
                # Убеждаемся, что оба datetime имеют часовой пояс
                if user.deadline.tzinfo is None:
                    deadline_aware = TZ.localize(user.deadline)
                else:
                    deadline_aware = user.deadline
                
                # Вычисляем разность и округляем до полных дней
                time_diff = deadline_aware - now
                total_seconds = time_diff.total_seconds()
                days_left = max(0, int(total_seconds / (24 * 60 * 60)))  # Округляем до полных дней
            else:
                days_left = 30  # Если дедлайн не установлен, показываем 30 дней
        else:
            # Если пользователь не найден, используем текущее время
            registration_date = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
            registration_status = "Ошибка регистрации"
            days_left = 0

        # --- 1️⃣ Инлайн-кнопки языков ---
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        lang_builder = InlineKeyboardBuilder()
        lang_builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
        lang_builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
        lang_builder.button(text="🇨🇳 中文", callback_data="lang_zh")
        lang_builder.button(text="🇰🇷 한국어", callback_data="lang_ko")
        lang_builder.button(text="🇺🇸 English", callback_data="lang_en")
        lang_builder.adjust(2, 2, 1)

        # --- 2️⃣ Формируем сообщение ---
        text = get_text("ru", "start_command",
                       user_id=user_id,
                       registration_date=registration_date,
                       registration_status=registration_status,
                       days_left=days_left)

        # --- 3️⃣ Отправляем сообщение с инлайн-кнопками ---
        await message.answer(
            text=text,
            reply_markup=lang_builder.as_markup()
        )
        
        # --- 5️⃣ Обновляем команды для пользователя ---
        from utils import update_user_commands
        await update_user_commands(user_id, "ru", self.bot)
    
    async def show_language_selection(self, message: types.Message, state: FSMContext):
        """Показывает выбор языка"""
        # Создаем или получаем пользователя
        user = await self.db_manager.get_user_by_tg_id(message.from_user.id)
        if not user:
            user = await self.db_manager.create_user(
                tg_id=message.from_user.id,
                username=message.from_user.username
            )
        
        if not user:
            await message.answer(get_text("ru", "error_occurred"))
            return
        
        language = user.language
        
        # Определяем статус регистрации
        from datetime import datetime, timedelta
        now = datetime.now()
        registration_time = user.created_at.replace(tzinfo=None)
        time_diff = now - registration_time
        
        if time_diff < timedelta(minutes=1):
            # Пользователь только что зарегистрировался
            registration_status = get_text(language, "just_registered")
        else:
            # Пользователь уже был зарегистрирован
            registration_status = get_text(language, "already_registered")
        
        # Формируем сообщение с информацией о регистрации
        registration_date = user.created_at.strftime("%d.%m.%Y %H:%M")
        
        # Проверяем что user_id не None
        user_id = user.tg_id if user.tg_id is not None else "Неизвестно"
        
        message_text = get_text(
            language, 
            "registration_info",
            user_id=user_id,
            registration_status=registration_status,
            registration_date=registration_date
        )
        
        # Создаем инлайн клавиатуру с языками
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        lang_builder = InlineKeyboardBuilder()
        lang_builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
        lang_builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
        lang_builder.button(text="🇨🇳 中文", callback_data="lang_zh")
        lang_builder.button(text="🇰🇷 한국어", callback_data="lang_ko")
        lang_builder.button(text="🇺🇸 English", callback_data="lang_en")
        lang_builder.adjust(2, 2, 1)  # 2 кнопки в первом ряду, 2 во втором, 1 в третьем
        
        # Сначала отправляем кнопки языков
        await message.answer(
            "🌍 Выберите язык:",
            reply_markup=lang_builder.as_markup()
        )
        
        # Затем отправляем информацию о регистрации (без кнопок)
        await message.answer(message_text)
        await state.set_state(RegistrationStates.waiting_for_language)
    
    async def show_main_menu(self, message: types.Message, language: str):
        """Показывает главное меню с кнопками Status и Help"""
        from aiogram.utils.keyboard import ReplyKeyboardBuilder
        
        builder = ReplyKeyboardBuilder()
        builder.button(text=get_text(language, "status_button"))
        builder.button(text=get_text(language, "help_button"))
        
        await message.answer(
            get_text(language, "main_menu_text"),
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
    
    
    async def handle_language_callback(self, callback: types.CallbackQuery):
        """Обработка выбора языка через инлайн кнопки"""
        # Проверяем блокировку
        if await self.block_inactive_callbacks(callback):
            return
            
        # Извлекаем язык из callback_data
        language_code = callback.data.split("_")[1]  # lang_ru -> ru
        
        # Логируем выбор языка
        await self.db_manager.log_user_action(callback.from_user.id, "language_selected", language_code)
        
        # Обновляем язык пользователя
        await self.db_manager.update_user_language(callback.from_user.id, language_code)
        logger.info(f"Пользователь {callback.from_user.id} выбрал язык: {language_code}")
        
        # Сохраняем язык в FSM state для использования в следующих шагах
        from aiogram.fsm.context import FSMContext
        from aiogram.fsm.storage.base import StorageKey
        
        # Создаем правильный ключ для FSM state
        storage_key = StorageKey(
            bot_id=callback.bot.id,
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id
        )
        state = FSMContext(storage=self.dp.storage, key=storage_key)
        await state.update_data(language=language_code)
        
        # Отвечаем на callback
        await callback.answer(f"Выбран язык: {language_code}")
        
        # Показываем важное сообщение с инлайн кнопкой
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        inline_builder = InlineKeyboardBuilder()
        inline_builder.button(text=get_text(language_code, "understood_month"), callback_data=f"understood_month_{language_code}")
        
        # Удаляем сообщение с кнопками языков
        await callback.message.delete()
        
        # Удаляем сообщение с информацией о регистрации (следующее сообщение)
        try:
            # Получаем следующий message_id (с информацией о регистрации)
            chat_id = callback.message.chat.id
            message_id = callback.message.message_id
            
            # Удаляем следующее сообщение (с информацией о регистрации)
            await callback.bot.delete_message(chat_id=chat_id, message_id=message_id + 1)
        except Exception as e:
            # Игнорируем ошибку если сообщение уже удалено
            pass
        
        # Показываем важное сообщение с новой инлайн кнопкой
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=get_text(language_code, "important_message"),
            reply_markup=inline_builder.as_markup()
        )
    
    async def handle_understood_month_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Понял' через инлайн callback"""
        # Извлекаем язык из callback_data
        if callback.data and callback.data.startswith("understood_month_"):
            language = callback.data.split("_", 2)[2]  # understood_month_ru -> ru
        else:
            # Fallback - получаем из базы данных
            user = await self.db_manager.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Создаем временный callback для совместимости
        temp_callback = types.CallbackQuery(
            id=callback.id,
            from_user=callback.from_user,
            chat_instance=str(callback.message.chat.id),
            message=callback.message
        )
        await self.button_handler.process_understood_month(temp_callback, state, language)
    
    async def handle_diagnosis_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка выбора диагноза через инлайн кнопки"""
        await self.button_handler.process_diagnosis_selection(callback, state)
    
    
    async def handle_show_documents_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Показать документы'"""
        await self.button_handler.process_show_documents(callback, state)
    
    async def handle_understood_examination_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Понял про обследование'"""
        await self.button_handler.process_understood_10_days(callback, state)
    
    async def handle_passed_examination_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Прошел обследование'"""
        await self.button_handler.process_passed_examination(callback, state)
    
    async def handle_not_passed_examination_callback(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Не прошел обследование'"""
        await self.button_handler.process_not_passed_examination(callback, state)
    
    
    async def process_language_selection(self, message: types.Message, state: FSMContext):
        """Обработка выбора языка"""
        text = message.text
        logger.info(f"DEBUG: process_language_selection вызван с текстом: {text}")
        
        # Определяем язык по тексту кнопки
        language_map = {
            "🇷🇺 Русский": "ru",
            "🇺🇿 O'zbek": "uz", 
            "🇨🇳 中文": "zh",
            "🇰🇷 한국어": "ko",
            "🇺🇸 English": "en"
        }
        
        language = language_map.get(text)
        if not language:
            await message.answer(get_text("ru", "invalid_selection"))
            return
        
        # Логируем выбор языка
        await self.db_manager.log_user_action(message.from_user.id, "language_selected", language)
        
        # Обновляем язык пользователя
        await self.db_manager.update_user_language(message.from_user.id, language)
        logger.info(f"Пользователь {message.from_user.id} выбрал язык: {language}")
        
        # Показываем согласие на обработку данных
        from aiogram.types import ReplyKeyboardRemove
        from aiogram.utils.keyboard import ReplyKeyboardBuilder
        
        builder = ReplyKeyboardBuilder()
        builder.button(text=get_text(language, "consent_button"))
        
        await message.answer(
            get_text(language, "consent"),
            reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
        
    
    
    async def cmd_status(self, message: types.Message, state: FSMContext):
        """Обработчик команды /status"""
        # Проверяем блокировку
        if await self.block_inactive_users(message):
            return
            
        user = await self.db_manager.get_user_by_tg_id(message.from_user.id)
        if not user:
            await message.answer(get_text("ru", "no_active_case"))
            return
        
        language = user.language
        
        # Получаем активность пользователя
        activity = await self.db_manager.get_user_activity(message.from_user.id)
        
        if not activity:
            # Если нет действий, показываем только регистрацию пользователя
            await self.button_handler.show_registration_status(message, user)
            return
        
        # Показываем статус с информацией о сроках
        await self.button_handler.show_detailed_status(message, user, activity[0])
    
    async def cmd_help(self, message: types.Message, state: FSMContext):
        """Обработчик команды /help"""
        # Проверяем блокировку
        if await self.block_inactive_users(message):
            return
            
        user = await self.db_manager.get_user_by_tg_id(message.from_user.id)
        language = user.language if user else "ru"
        
        from aiogram.types import ReplyKeyboardRemove
        
        await message.answer(
            get_text(language, "help_text"),
            reply_markup=ReplyKeyboardRemove()
        )
    
    async def cmd_test_cycle(self, message: types.Message, state: FSMContext):
        """Тестирует цикл уведомлений (5–10–15–20–25–30–31 день) - ТЕСТОВАЯ ФУНКЦИЯ"""
        user_id = message.from_user.id
        await message.answer("✅ Тест запущен: уведомления будут каждые 10 секунд")

        from scheduler import send_test_reminder, block_test_user
        
        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=10),
            args=[user_id, 5],
            id=f"rem_5_{user_id}", replace_existing=True)

        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=20),
            args=[user_id, 10],
            id=f"rem_10_{user_id}", replace_existing=True)

        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=30),
            args=[user_id, 15],
            id=f"rem_15_{user_id}", replace_existing=True)

        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=40),
            args=[user_id, 20],
            id=f"rem_20_{user_id}", replace_existing=True)

        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=50),
            args=[user_id, 25],
            id=f"rem_25_{user_id}", replace_existing=True)

        self.scheduler.add_job(send_test_reminder, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=60),
            args=[user_id, 30],
            id=f"rem_30_{user_id}", replace_existing=True)

        # 🔥 31-й день → через 70 секунд (для теста)
        self.scheduler.add_job(block_test_user, "date",
            run_date=datetime.now(TZ) + timedelta(seconds=70),
            args=[user_id],
            id=f"block_{user_id}", replace_existing=True)
    
    # Тестовые функции
    async def send_reminder(self, user_id: int, day: int):
        """Отправляет тестовое напоминание"""
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=f"📅 Напоминание (тест): прошло {day} дней"
            )
            logger.info(f"🔔 Напоминание для {day} дней отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")

    async def block_user_after_31_days(self, user_id: int):
        """Блокирует пользователя (тест)"""
        async with self.db_manager.session_maker() as session:
            from sqlalchemy import select
            from database import User
            
            result = await session.execute(select(User).where(User.tg_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                return

            user.blocked = True
            await session.commit()

        try:
            await self.bot.send_message(
                chat_id=user_id,
                text="⛔️ (ТЕСТ) Доступ к боту закрыт. Прошло 31 день."
            )
            logger.info(f"🚫 Пользователь {user_id} заблокирован (тестовый режим)")
        except Exception as e:
            logger.error(f"Ошибка при блокировке пользователя {user_id}: {e}")
    
    # Обработчики кнопок
    
    
    async def start_polling(self):
        """Запускает бота"""
        try:
            # Инициализируем базу данных
            await init_db()
            logger.info("База данных инициализирована")
            
            # Настраиваем планировщик
            self.scheduler = setup_scheduler(self.bot)
            logger.info("Планировщик настроен")
            
            # Запускаем бота
            logger.info("Бот запускается...")
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
        finally:
            if hasattr(self, 'scheduler'):
                self.scheduler.shutdown()
            await self.bot.session.close()

async def handle(request):
    """Простой ответ для проверки Render, что бот активен"""
    return web.Response(text="✅ Bot is alive and running")

def start_keepalive_server():
    """Запускает keep-alive сервер для Render"""
    import os
    port = int(os.environ.get("PORT", 8080))  # Render задает порт через переменную PORT
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, host="0.0.0.0", port=port)


def main():
    """Главная функция"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    bot = TelegramBot()
    
    try:
        asyncio.run(bot.start_polling())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    threading.Thread(target=start_keepalive_server, daemon=True).start()
    main()
