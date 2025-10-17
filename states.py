#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Состояния FSM для бота
"""

from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    """Состояния процесса регистрации"""
    waiting_for_language = State()
    waiting_for_consent = State()

class DiagnosisStates(StatesGroup):
    """Состояния процесса выбора диагноза"""
    waiting_for_understanding = State()
    waiting_for_result = State()
