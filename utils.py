#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вспомогательные функции для бота
"""

from aiogram import Bot
from aiogram.types import BotCommand, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from texts import get_text

async def update_user_commands(user_id: int, language: str, bot: Bot):
    """Обновляет команды для пользователя"""
    commands = [
        BotCommand(command="start", description=get_text(language, "start_cmd_desc")),
        BotCommand(command="status", description=get_text(language, "status_cmd_desc")),
        BotCommand(command="help", description=get_text(language, "help_cmd_desc")),
    ]
    await bot.set_my_commands(commands, scope={"type": "chat", "chat_id": user_id})

def get_diagnosis_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру выбора диагноза"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text=get_text(language, "tuberculosis"))
    builder.button(text=get_text(language, "syphilis"))
    builder.button(text=get_text(language, "hiv"))
    builder.button(text=get_text(language, "drug_addiction"))
    
    builder.adjust(2, 2)  # 2 кнопки в каждом ряду
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_diagnosis_actions_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру действий после выбора диагноза"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text=get_text(language, "show_documents"))
    builder.button(text=get_text(language, "understood_examination"))
    
    builder.adjust(1, 1)  # По одной кнопке в ряду
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_examination_result_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру результата обследования"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text=get_text(language, "passed_examination"))
    builder.button(text=get_text(language, "not_passed_examination"))
    builder.button(text=get_text(language, "result_received"))
    
    builder.adjust(1, 1, 1)  # По одной кнопке в каждом ряду
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def get_keyboard_for_user(user_id: int, language: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру для пользователя"""
    builder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки в зависимости от языка
    start_text = get_text(language, "start_button")
    status_text = get_text(language, "status_button") 
    help_text = get_text(language, "help_button")
    
    builder.button(text=start_text)
    builder.button(text=status_text)
    builder.button(text=help_text)
    
    builder.adjust(1, 1, 1)
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_language_keyboard() -> ReplyKeyboardMarkup:
    """Создает клавиатуру выбора языка"""
    from aiogram.utils.keyboard import ReplyKeyboardBuilder
    
    builder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки языков
    builder.button(text="🇷🇺 Русский")
    builder.button(text="🇺🇿 O'zbek") 
    builder.button(text="🇨🇳 中文")
    builder.button(text="🇰🇷 한국어")
    builder.button(text="🇺🇸 English")
    
    # Настройки клавиатуры
    builder.adjust(2, 2, 1)  # 2 кнопки в первом ряду, 2 во втором, 1 в третьем
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
