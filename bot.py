#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот для уведомлений о дообследовании
Новый ООП подход - использует классы для лучшей организации кода
"""

from telegram_bot import TelegramBot
import logging

def main():
    """Главная функция - запуск бота"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота с ООП архитектурой...")
    
    bot = TelegramBot()
    
    try:
        import asyncio
        asyncio.run(bot.start_polling())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()