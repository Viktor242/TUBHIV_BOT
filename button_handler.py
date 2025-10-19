#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обработчик кнопок - класс для обработки всех кнопок и callback'ов
"""

import logging
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logger = logging.getLogger(__name__)

from database_manager import DatabaseManager
from texts import get_text
from utils import get_diagnosis_keyboard, get_diagnosis_actions_keyboard, get_examination_result_keyboard, get_keyboard_for_user, update_user_commands, get_language_keyboard
from states import RegistrationStates, DiagnosisStates

import logging
logger = logging.getLogger(__name__)

class ButtonHandler:
    """Класс для обработки всех кнопок и callback'ов"""
    
    def __init__(self, database_manager: DatabaseManager, bot):
        self.db = database_manager
        self.bot = bot
    
    async def process_language_selection(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка выбора языка"""
        language = callback.data.split("_")[1]  # ru, uz, zh, ko, en
        
        # Логируем выбор языка
        await self.db.log_user_action(callback.from_user.id, "language_selected", language)
        
        # Обновляем язык пользователя
        await self.db.update_user_language(callback.from_user.id, language)
        logger.info(f"Пользователь {callback.from_user.id} выбрал язык: {language}")
        
        # Обновляем команды для пользователя
        await update_user_commands(callback.from_user.id, language, self.bot)
        
        # Показываем важное сообщение сразу после выбора языка
        builder = ReplyKeyboardBuilder()
        builder.button(text=get_text(language, "understood_month"))
        important_kb = builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        
        await callback.message.answer(
            get_text(language, "important_message"),
            reply_markup=important_kb
        )
        await state.set_state(RegistrationStates.waiting_for_consent)
    
    async def process_understood_month(self, callback: types.CallbackQuery, state: FSMContext, language: str = None):
        """Обработка понимания про месяц"""
        # Логируем действие
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "understood_month")
        
        # Используем переданный язык или получаем из базы данных
        if language is None:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Отладочная информация
        logger.info(f"DEBUG: process_understood_month - user_id: {callback.from_user.id}, language: {language}")
        
        # Отвечаем на callback сразу
        await self.bot.answer_callback_query(callback.id)
        
        # Создаем инлайн клавиатуру с диагнозами
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        diagnosis_builder = InlineKeyboardBuilder()
        diagnosis_builder.button(text=get_text(language, "tuberculosis"), callback_data="diag_tuberculosis")
        diagnosis_builder.button(text=get_text(language, "syphilis"), callback_data="diag_syphilis")
        diagnosis_builder.button(text=get_text(language, "hiv"), callback_data="diag_hiv")
        diagnosis_builder.button(text=get_text(language, "drug_addiction"), callback_data="diag_drug_addiction")
        diagnosis_builder.adjust(2, 2)  # 2 кнопки в каждом ряду
        
        # Редактируем сообщение вместо отправки нового
        try:
            await callback.message.edit_text(
                text=get_text(language, "category_select"),
                reply_markup=diagnosis_builder.as_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отредактировать сообщение после 'Понял': {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await self.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text(language, "category_select"),
                reply_markup=diagnosis_builder.as_markup()
            )
    
    async def process_not_passed_examination(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Не прошел обследование'"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "not_passed_examination")
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Отвечаем на callback сразу
        await self.bot.answer_callback_query(callback.id)
        
        # Возвращаемся к выбору диагноза (меню из 4 диагнозов)
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        diagnosis_builder = InlineKeyboardBuilder()
        diagnosis_builder.button(text=get_text(language, "tuberculosis"), callback_data="diag_tuberculosis")
        diagnosis_builder.button(text=get_text(language, "syphilis"), callback_data="diag_syphilis")
        diagnosis_builder.button(text=get_text(language, "hiv"), callback_data="diag_hiv")
        diagnosis_builder.button(text=get_text(language, "drug_addiction"), callback_data="diag_drug_addiction")
        diagnosis_builder.adjust(2, 2)  # 2 кнопки в каждом ряду
        
        # Редактируем сообщение вместо отправки нового
        try:
            await callback.message.edit_text(
                text=get_text(language, "category_select"),
                reply_markup=diagnosis_builder.as_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отредактировать сообщение: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await self.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text(language, "category_select"),
                reply_markup=diagnosis_builder.as_markup()
            )
    
    async def process_diagnosis_selection(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка выбора диагноза через инлайн кнопки"""
        # Получаем диагноз из callback_data
        if callback.data and callback.data.startswith("diag_"):
            diagnosis = callback.data.split("_", 1)[1]
        else:
            diagnosis = "tuberculosis"  # По умолчанию
        
        # Логируем выбор диагноза
        await self.db.log_user_action(callback.from_user.id, "diagnosis_chosen", diagnosis)
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        logger.info(f"DEBUG: process_diagnosis_selection - user_id: {callback.from_user.id}, language: {language}, diagnosis: {diagnosis}")
        
        # Отвечаем на callback сразу
        await self.bot.answer_callback_query(callback.id)
        
        # Создаем инлайн кнопки действий
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        actions_builder = InlineKeyboardBuilder()
        actions_builder.button(text=get_text(language, "show_documents"), callback_data="show_documents")
        actions_builder.button(text=get_text(language, "understood_examination"), callback_data="understood_examination")
        actions_builder.adjust(1, 1)  # По одной кнопке в ряду
        
        # Формируем сообщение с описанием диагноза
        diagnosis_info = get_text(language, f"{diagnosis}_info")
        message_text = f"{get_text(language, 'diagnosis_found')}\n\n{diagnosis_info}"
        
        # Редактируем сообщение вместо отправки нового
        try:
            await callback.message.edit_text(
                text=message_text,
                reply_markup=actions_builder.as_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отредактировать сообщение: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await self.bot.send_message(
                chat_id=callback.message.chat.id,
                text=message_text,
                reply_markup=actions_builder.as_markup()
            )
        await state.set_state(DiagnosisStates.waiting_for_understanding)
    
    async def process_understood_10_days(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка понимания про 10 дней"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "understood_10_days")
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Отвечаем на callback сразу
        await self.bot.answer_callback_query(callback.id)
        
        # Создаем инлайн кнопки вопроса о дообследовании
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        examination_builder = InlineKeyboardBuilder()
        examination_builder.button(text=get_text(language, "passed_examination"), callback_data="passed_examination")
        examination_builder.button(text=get_text(language, "not_passed_examination"), callback_data="not_passed_examination")
        examination_builder.adjust(1, 1)  # По одной кнопке в ряду
        
        # Редактируем сообщение вместо удаления
        try:
            await callback.message.edit_text(
                text=get_text(language, "examination_question"),
                reply_markup=examination_builder.as_markup()
            )
        except Exception as e:
            logger.error(f"Не удалось отредактировать сообщение: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await self.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text(language, "examination_question"),
                reply_markup=examination_builder.as_markup()
            )
        
        await state.set_state(DiagnosisStates.waiting_for_result)
    
    async def process_understood_examination(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка понимания обследования"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "understood_examination")
        
        user = await self.db.get_user_by_tg_id(callback.from_user.id)
        language = user.language if user else "ru"
        
        # Показываем сообщение о результате
        result_kb = get_examination_result_keyboard(language)
        
        await callback.message.answer(
            get_text(language, "result_received_message"),
            reply_markup=result_kb
        )
        await state.set_state(DiagnosisStates.waiting_for_result)
    
    async def process_passed_examination(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Прошел обследование'"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "passed_examination")
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Отвечаем на callback сразу
        await self.bot.answer_callback_query(callback.id)
        
        # Редактируем сообщение с текстом о справке
        try:
            await callback.message.edit_text(
                text=get_text(language, "waiting_certificate")
            )
        except Exception as e:
            logger.error(f"Не удалось отредактировать сообщение: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await self.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text(language, "waiting_certificate")
            )
        
        await state.clear()
    
    async def process_not_passed_examination_result(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Не прошел обследование' из результата"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "not_passed_examination_result")
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Показываем сообщение о необходимости пройти обследование
        from aiogram.types import ReplyKeyboardRemove
        
        await callback.message.answer(
            get_text(language, "examination_required"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    
    async def process_result_received(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Получил результат'"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "result_received")
        
        user = await self.db.get_user_by_tg_id(callback.from_user.id)
        language = user.language if user else "ru"
        
        # Удаляем сообщение с кнопками
        await callback.message.delete()
        
        # Показываем сообщение об успехе
        await self.bot.send_message(
            chat_id=callback.message.chat.id,
            text=get_text(language, "result_received_success")
        )
        await state.clear()
    
    async def process_status_button(self, message: types.Message, state: FSMContext):
        """Обработка кнопки 'Статус' - показывает всплывающее уведомление"""
        await self.db.log_user_action(message.from_user.id, "button_pressed", "status")
        
        user = await self.db.get_user_by_tg_id(message.from_user.id)
        if not user:
            # Создаем inline кнопку для всплывающего уведомления
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=get_text("ru", "show_status"), callback_data="show_status_popup")
            ]])
            await message.answer(get_text("ru", "click_for_status"), reply_markup=keyboard)
            return
        
        # Получаем последнее действие пользователя
        activity = await self.db.get_user_activity(message.from_user.id)
        
        # Формируем сообщение о статусе
        language = user.language
        from datetime import datetime, timedelta
        
        # Вычисляем дни
        now = datetime.now()
        days_passed = (now - user.created_at).days
        days_remaining = max(0, 31 - days_passed)
        
        # Создаем текст статуса
        if not activity:
            # Если нет действий, показываем только регистрацию пользователя
            status_text = (
                f"🆔 {get_text(language, 'user_id')}: {user.tg_id}\n"
                f"📅 {get_text(language, 'registration_date')}: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"✅ {get_text(language, 'already_registered')}\n"
                f"⏰ {get_text(language, 'days_left', days=days_remaining)}"
            )
        else:
            # Если есть активность, показываем детальный статус
            activity_data = activity[0]
            registration_date = user.created_at.strftime("%d.%m.%Y %H:%M")
            
            if activity_data.action_type == "Выбор диагноза" and activity_data.deadline_at:
                # Дата выбора диагноза
                diagnosis_date = activity_data.timestamp.strftime("%d.%m.%Y %H:%M")
                
                # Срок окончания (30 дней с выбора диагноза)
                deadline_date = activity_data.deadline_at.strftime("%d.%m.%Y")
                
                # Сколько дней осталось
                import pytz
                TZ = pytz.timezone("Asia/Vladivostok")
                now_tz = datetime.now(TZ)
                days_left = (activity_data.deadline_at - now_tz).days
                
                if days_left > 0:
                    days_text = get_text(language, "days_left", days=days_left)
                elif days_left == 0:
                    days_text = get_text(language, "last_day")
                else:
                    days_text = get_text(language, "overdue", days=abs(days_left))
                
                status_text = (
                    f"👤 {get_text(language, 'user_id')}: {user.tg_id}\n"
                    f"📅 {get_text(language, 'registration_date')}: {registration_date}\n"
                    f"🩺 {get_text(language, 'diagnosis_date')}: {diagnosis_date}\n"
                    f"⏰ {get_text(language, 'deadline_date')}: {deadline_date}\n"
                    f"📆 {days_text}"
                )
            else:
                status_text = (
                    f"👤 {get_text(language, 'user_id')}: {user.tg_id}\n"
                    f"📅 {get_text(language, 'registration_date')}: {registration_date}\n"
                    f"🩺 {get_text(language, 'status')}: {get_text(language, 'waiting_diagnosis')}"
                )
        
        # Создаем inline кнопку для всплывающего уведомления
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=get_text(language, "show_status"), callback_data="show_status_popup")
        ]])
        await message.answer(get_text(language, "click_for_status"), reply_markup=keyboard)
    
    async def process_help_button(self, message: types.Message, state: FSMContext):
        """Обработка кнопки 'Помощь' - показывает всплывающее уведомление"""
        await self.db.log_user_action(message.from_user.id, "button_pressed", "help")
        
        user = await self.db.get_user_by_tg_id(message.from_user.id)
        language = user.language if user else "ru"
        
        # Создаем inline кнопку для всплывающего уведомления
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=get_text(language, "show_help"), callback_data="show_help_popup")
        ]])
        await message.answer(get_text(language, "click_for_help"), reply_markup=keyboard)
    
    async def process_show_documents(self, callback: types.CallbackQuery, state: FSMContext):
        """Обработка кнопки 'Показать документы'"""
        await self.db.log_user_action(callback.from_user.id, "button_pressed", "show_documents")
        
        # Получаем язык из FSM state (приоритет) или из базы данных (fallback)
        state_data = await state.get_data()
        language = state_data.get('language')
        if not language:
            user = await self.db.get_user_by_tg_id(callback.from_user.id)
            language = user.language if user else "ru"
        
        # Показываем всплывающее сообщение с документами
        await callback.answer(
            text=get_text(language, "documents_reminder"),
            show_alert=True
        )
    
    async def show_registration_status(self, message, user):
        """Показывает статус регистрации пользователя"""
        language = user.language
        from aiogram.types import ReplyKeyboardRemove
        from datetime import datetime, timedelta
        import pytz
        
        # Вычисляем дни до дедлайна
        TZ = pytz.timezone("Asia/Vladivostok")
        now = datetime.now(TZ)
        
        if user.deadline:
            # Убеждаемся, что оба datetime имеют часовой пояс
            if user.deadline.tzinfo is None:
                deadline_aware = TZ.localize(user.deadline)
            else:
                deadline_aware = user.deadline
            
            # Вычисляем разность и округляем до полных дней
            time_diff = deadline_aware - now
            total_seconds = time_diff.total_seconds()
            days_remaining = max(0, int(total_seconds / (24 * 60 * 60)))  # Округляем до полных дней
        else:
            days_remaining = 30  # Если дедлайн не установлен, показываем 30 дней
        
        # Правильно обрабатываем время регистрации с часовым поясом
        if user.created_at:
            if user.created_at.tzinfo is None:
                # Если время без часового пояса, считаем его локальным временем Владивостока
                registration_time = user.created_at.strftime('%d.%m.%Y %H:%M')
            else:
                # Конвертируем в локальное время Владивостока
                local_time = user.created_at.astimezone(TZ)
                registration_time = local_time.strftime('%d.%m.%Y %H:%M')
        else:
            registration_time = datetime.now(TZ).strftime('%d.%m.%Y %H:%M')
        
        # Красивое сообщение со статусом пользователя
        from texts import get_text
        status_message = (
            f"🆔 {get_text(language, 'user_id')}: {user.tg_id}\n"
            f"📅 {get_text(language, 'registration_date')}: {registration_time}\n"
            f"✅ {get_text(language, 'already_registered')}\n"
            f"⏰ {get_text(language, 'days_left', days=days_remaining)}"
        )
        
        await message.answer(status_message, reply_markup=ReplyKeyboardRemove())
    
    async def show_detailed_status(self, message, user, activity):
        """Показывает детальный статус с информацией о сроках"""
        from datetime import datetime, timedelta
        import pytz
        
        language = user.language
        from aiogram.types import ReplyKeyboardRemove
        TZ = pytz.timezone("Asia/Vladivostok")
        
        # Правильно обрабатываем время регистрации с часовым поясом
        if user.created_at:
            if user.created_at.tzinfo is None:
                registration_date = user.created_at.strftime("%d.%m.%Y %H:%M")
            else:
                local_time = user.created_at.astimezone(TZ)
                registration_date = local_time.strftime("%d.%m.%Y %H:%M")
        else:
            registration_date = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
        
        # Проверяем есть ли информация о диагнозе
        if activity.action_type == "Выбор диагноза" and activity.deadline_at:
            # Дата выбора диагноза (правильно обрабатываем часовой пояс)
            if activity.timestamp.tzinfo is None:
                diagnosis_date = activity.timestamp.strftime("%d.%m.%Y %H:%M")
            else:
                local_time = activity.timestamp.astimezone(TZ)
                diagnosis_date = local_time.strftime("%d.%m.%Y %H:%M")
            
            # Срок окончания (30 дней с выбора диагноза)
            deadline_date = activity.deadline_at.strftime("%d.%m.%Y")
            
            # Сколько дней осталось
            now = datetime.now(TZ)
            days_left = (activity.deadline_at - now).days
            
            if days_left > 0:
                days_text = get_text(language, "days_left").format(days=days_left)
            elif days_left == 0:
                days_text = get_text(language, "last_day")
            else:
                days_text = get_text(language, "overdue").format(days=abs(days_left))
            
            # Красивое сообщение со статусом обследования
            from texts import get_text
            status_message = (
                f"👤 {get_text(language, 'user_id')}: {user.tg_id}\n"
                f"📅 {get_text(language, 'registration_date')}: {registration_date}\n"
                f"🩺 {get_text(language, 'diagnosis_date')}: {diagnosis_date}\n"
                f"⏰ {get_text(language, 'deadline_date')}: {deadline_date}\n"
                f"📆 {days_text}\n\n"
                f"⚠️ {get_text(language, 'examination_required')}"
            )
            
        else:
            # Если нет информации о диагнозе
            status_message = (
                f"👤 {get_text(language, 'user_id')}: {user.tg_id}\n"
                f"📅 {get_text(language, 'registration_date')}: {registration_date}\n"
                f"🩺 {get_text(language, 'status')}: {get_text(language, 'waiting_diagnosis')}\n\n"
                f"{get_text(language, 'choose_diagnosis')}"
            )
        
        await message.answer(status_message, reply_markup=ReplyKeyboardRemove())
