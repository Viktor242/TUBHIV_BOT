#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тексты и кнопки для бота на 5 языках
"""

# Многоязычные тексты
TEXTS = {
    "ru": {
        # Выбор языка
        "language_select": "🌍 Выберите язык:",
        "your_id": "🆔 Ваш ID: {user_id}",
        "registered_new": "Вы зарегистрированы.",
        "registered_existing": "Вы уже зарегистрированы.",
        
        # Согласие
        "consent": "Для продолжения работы с ботом необходимо ваше согласие на обработку персональных данных.\n\nНажмите кнопку ниже, чтобы продолжить.",
        "consent_button": "✅ Согласен",
        
        # Важное сообщение
        "important_message": "⚠️ ВАЖНОЕ СООБЩЕНИЕ\n\nПо Вам уже передали сведения в РОСПОТРЕБНАДЗОР. Если Вы не пройдете дообследования, Вы получите представление о НЕЖЕЛАТЕЛЬНОМ пребывании в Российской Федерации. Не медлите! У Вас есть один месяц!",
        "understood_month": "✅ Понял, месяц",
        
        # Выбор диагноза
        "diagnosis_found": "📋 У ВАС ВЫЯВИЛИ\nВыберите свою кнопку:",
        "category_select": "Выбери категорию:",
        
        # Диагнозы
        "tuberculosis": "🫁 Туберкулёз",
        "syphilis": "🧬 Сифилис", 
        "hiv": "🧫 ВИЧ",
        "drug_addiction": "💊 Наркомания",
        
        # Информация о диагнозах
        "tuberculosis_info": (
            "🫁 ТУБЕРКУЛЁЗ\n\n"
            "Туберкулез- крайне опасное и заразное заболевание, которое может повлечь за собой смерть. "
            "Оно передается воздушно- капельным путем. При своевременной диагностике (Манту, Диаскин-тест, флюорографии) можно вылечить навсегда! "
            "Поэтому не переживайте, и скорее идите в Противотуберкулезный диспансер с нашим направлением в ГБУЗ ПКПТД по адресу Владивосток, 4-я Флотская 37/39, "
            "у Вас есть 10 дней, чтобы дойти до врача фтизиатра. Возможно, Вам назначат посев мокроты и компьютерную томографию органов грудной полости."
        ),
        "syphilis_info": (
            "🧬 СИФИЛИС\n\n"
            "Сифилис- опасное инфекционное заболевание передающееся половым путем. Поддается лечению! "
            "Поэтому не переживайте и скорее идите в Кожно-венерологический диспансер с нашим направлением с направлением ГБУЗ ККВД по адресу Владивосток, Гамарника 18 В, "
            "у Вас есть 10 дней, чтобы дойти до врача дерматовенеролога."
        ),
        "hiv_info": (
            "🧫 ВИЧ-ИНФЕКЦИЯ\n\n"
            "ВИЧ-инфекция- заболевание, вызванное вирусом иммунодефицита человека. Вирус уничтожает клетки иммунитета, "
            "которые помогают организму справиться с болезнетворными микроорганизмами. Антиретровирусная терапия продлила жизнь этих пациентов, "
            "подавляя размножение этого вируса. Лечение в России данными препаратами невозможно, по юридическим причинам. "
            "Для консультации Вам необходимо обратиться Краевая клиническая больница № 2, центр по профилактике и борьбе со СПИД и инфекционными заболеваниями по адресу Босисенко 50"
        ),
        "drug_addiction_info": (
            "💊 НАРКОМАНИЯ\n\n"
            "Ваш биологический материал поехал в Краевой Наркологический диспансер. Помните! Положительный результат может не подтвердится, "
            "поэтому не переживайте, ждите результата. Если результат окажется положительным, Вам лучше поехать домой и начать лечение, "
            "а также Вы можете обратиться в Краевой Наркологический диспансер по адресу Станюковича 53 для оспаривания результата. Всего наилучшего!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 Не забудьте с собой взять:\n• паспорт\n• миграционная карта\n• виза\n• регистрация",
        "understood_10_days": "✅ Понял, 10 дней",
        "understood_10_days_examination": "Понял, 10 дней пройти обследование",
        "show_documents": "📋 Документы",
        "passed_examination": "✅ Прошел",
        "not_passed_examination": "❌ Нет",
        "waiting_certificate": "Ждем Вас со справкой в ООО МО «Лотос» по адресу Владивосток, Стрелковая 23А",
        
        # Кнопки меню
        "start_button": "🚀 Старт",
        "status_button": "📊 Статус",
        "help_button": "❓ Помощь",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 Открыть меню",
        "cmd_status_desc": "📊 Статус регистрации", 
        "cmd_help_desc": "❓ Как работает бот?",
        
        # Результат
        "result_received": "✅ Результат получен",
        "result_received_message": "🎉 Отлично! Результат получен. Если нужно пройти другое обследование, выбери категорию:",
        
        # Помощь
        "help": "❓ Помощь",
        "help_text": (
    "📚 СПРАВКА ПО БОТУ\n\n"
    "Команды:\n"
    "/start - Начать работу с ботом\n"
    "/status - Узнать статус регистрации\n"
    "/help - Показать эту справку\n\n"
    "У тебя есть 10 дней, чтобы дойти по направлению, а в течение месяца мы отправим тебе результаты комиссии!"
        ),
        
        # Статус
        "status_text": (
    "📊 СТАТУС ОБСЛЕДОВАНИЯ\n\n"
    "🆔 Ваш ID: {user_id}\n"
    "Диагноз: {category}\n"
    "Дата первого посещения: {registered_at}\n"
    "Прошло дней: {days_passed}\n"
    "Осталось дней: {days_remaining}\n"
    "Дата окончания: {deadline_at}\n\n"
    "{next_reminder_text}"
        ),
        "no_active_case": "У тебя нет активных обследований. Нажми /start, чтобы начать.",
        "case_stopped": "✅ Напоминания остановлены. Если нужно начать заново, нажми /start",
        "expired_status": "⏰ СРОК ИСТЕК\n\n🆔 Ваш ID: {user_id}\nДиагноз: {category}\nДата первого посещения: {registered_at}\n\nСроки по дообследованию закончены. Ваши документы поданы в миграционную службу.",
        
        # Тексты напоминаний
        "next_reminder_5": "Следующее напоминание: на 5-й день (через {next_reminder} {day_word})",
        "next_reminder_10": "Следующее напоминание: на 10-й день (через {next_reminder} {day_word})",
        "next_reminder_15": "Следующее напоминание: на 15-й день (через {next_reminder} {day_word})",
        "next_reminder_20": "Следующее напоминание: на 20-й день (через {next_reminder} {day_word})",
        "next_reminder_25": "Следующее напоминание: на 25-й день (через {next_reminder} {day_word})",
        "next_reminder_30": "Следующее напоминание: на 30-й день (через {next_reminder} {day_word}) - ФИНАЛЬНОЕ",
        "all_reminders_sent": "Все напоминания отправлены. Обследование завершено.",
        
        # Сообщения об ошибках
        "error_occurred": "Произошла ошибка. Пожалуйста, нажмите /start заново.",
        "choose_category": "Пожалуйста, выберите категорию из предложенных кнопок.",
        "no_active_examinations": "У Вас нет активных обследований.",
        "registration_status": "📊 СТАТУС РЕГИСТРАЦИИ\n\n🆔 Ваш ID: {user_id}\nДата регистрации: {registered_at}\nПрошло дней с регистрации: {days_since_registration}\n\nУ Вас пока нет активных обследований. Нажмите /start для начала.",
        
        # Напоминания
        "reminder_template": (
            "⏰ НАПОМИНАНИЕ!\n\n"
            "Прошло {days} дней с начала наблюдения по диагнозу: {category}\n"
            "Осталось дней до окончания срока: {remaining}\n\n"
            "Пожалуйста, не забудь вовремя пройти обследование!"
        ),
        "final_reminder": (
            "⚠️ ВНИМАНИЕ!\n\n"
            "Сроки по дообследованию закончены, Ваши документы поданы в миграционную службу.\n\n"
            "Через 1 день доступ к боту будет ограничен."
        ),
        "bot_liquidation_message": (
            "🚫 ЛИКВИДАЦИЯ БОТА\n\n"
            "Сроки по дообследованию полностью закончены.\n"
            "Ваши данные переданы в миграционную службу.\n\n"
            "Доступ к боту ограничен."
        ),
        
        # Переводы типов действий
        "action_bot_started": "Запуск бота",
        "action_language_selected": "Выбор языка",
        "action_button_pressed": "Нажатие кнопки",
        "action_diagnosis_chosen": "Выбор диагноза",
        "action_examination_result": "Результат обследования",
        
        # Переводы данных действий
        "action_data_understood_month": "Понял про месяц",
        "action_data_show_documents": "Показать документы",
        "action_data_understood_10_days": "Понял про 10 дней",
        "action_data_passed_examination": "Прошел обследование",
        "action_data_not_passed_examination": "Не прошел обследование",
        "action_data_tuberculosis": "Туберкулез",
        "action_data_syphilis": "Сифилис",
        "action_data_hiv": "ВИЧ-инфекция",
        "action_data_drug_addiction": "Наркомания",
        "action_data_important_message": "Важное сообщение",
        "action_data_show_diagnosis_menu": "У вас выявили",
        "action_data_show_help": "Помощь"
    },
    
    "uz": {
        # Выбор языка
        "language_select": "🌍 Tilni tanlang:",
        "your_id": "🆔 Sizning ID: {user_id}",
        "registered_new": "Siz ro'yxatdan o'tdingiz.",
        "registered_existing": "Siz allaqachon ro'yxatdan o'tgansiz.",
        
        # Согласие
        "consent": "Bot bilan ishlashni davom ettirish uchun shaxsiy ma'lumotlarni qayta ishlashga roziligingiz kerak.\n\nDavom etish uchun quyidagi tugmani bosing.",
        "consent_button": "✅ Roziman",
        
        # Важное сообщение
        "important_message": "⚠️ MUHIM XABAR\n\nSiz haqingizda ma'lumotlar ROSPOTREBNADZORga uzatilgan. Agar siz qo'shimcha tekshiruvlarni o'tkazmasangiz, Rossiya Federatsiyasida istalmagan qolish haqida ta'kidnoma olasiz. Shoshiling! Sizda bir oy bor!",
        "understood_month": "✅ Tushundim, oy",
        
        # Выбор диагноза
        "diagnosis_found": "📋 SIZDA ANIQLANDI\nO'z tugmangizni tanlang:",
        "category_select": "Kategoriyani tanlang:",
        
        # Диагнозы
        "tuberculosis": "🫁 Sil kasalligi",
        "syphilis": "🧬 Sifilis", 
        "hiv": "🧫 OIV",
        "drug_addiction": "💊 Giynomaniya",
        
        # Информация о диагнозах (упрощенная версия на узбекском)
        "tuberculosis_info": "🫁 SIL KASALLIGI\n\nSil kasalligi - juda xavfli va yuqumli kasallik bo'lib, o'limga olib kelishi mumkin. Havo orqali yuqadi. Vaqtida tashxis qo'yilsa (Mantu, Diaskin-test, flyuorografiya) butunlay davolash mumkin!",
        "syphilis_info": "🧬 SIFILIS\n\nSifilis - jinsiy yo'l bilan yuqadigan xavfli yuqumli kasallik. Davolash mumkin!",
        "hiv_info": "🧫 OIV-INFECTSIYA\n\nOIV-infektsiya - inson immunitet tanqisligi virusi tufayli yuzaga keladigan kasallik.",
        "drug_addiction_info": (
            "💊 GIYNOMANIYA\n\n"
            "Sizning biologik materialingiz Viloyat narkologik dispanseriga yuborildi. Eslab qoling! "
            "Ijobiy natija tasdiqlanmasligi mumkin, shuning uchun tashvishlanmang, natijani kuting. "
            "Agar natija ijobiy bo'lsa, uyga qaytib, davolanishni boshlash yaxshiroq bo'ladi, "
            "shuningdek, natijani rad etish uchun Stanjukovich 53 manzilidagi Viloyat narkologik dispanseriga murojaat qilishingiz mumkin. "
            "Omad tilaymiz!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 O'zingiz bilan olib kelishni unutmang:\n• pasport\n• migratsiya karta\n• viza\n• ro'yxatdan o'tish",
        "understood_10_days": "✅ Tushundim, 10 kun",
        "understood_10_days_examination": "Tushundim, 10 kun tekshiruvni o'tkazish",
        "show_documents": "📋 Hujjatlar",
        "passed_examination": "✅ O'tkazdim",
        "not_passed_examination": "❌ Yo'q",
        "waiting_certificate": "Sizni OOO MO «Lotos»da, Vladivostok, Strelkovaya 23A manzilida spravka bilan kutamiz",
        
        # Кнопки меню
        "start_button": "🚀 Boshlash",
        "status_button": "📊 Holat",
        "help_button": "❓ Yordam",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 Menyuni ochish",
        "cmd_status_desc": "📊 Ro'yxatdan o'tish holati",
        "cmd_help_desc": "❓ Bot qanday ishlaydi?",
        
        # Результат
        "result_received": "✅ Natija olindi",
        "result_received_message": "🎉 Ajoyib! Natija olindi. Agar boshqa tekshiruvdan o'tish kerak bo'lsa, kategoriyani tanlang:",
        
        # Помощь
        "help": "❓ Yordam",
        "help_text": "📚 BOT HAQIDA MA'LUMOT\n\nBuyruqlar:\n/start - Bot bilan ishlashni boshlash\n/status - Ro'yxatdan o'tish holatini bilish\n/help - Bu yordamni ko'rsatish\n\nSizda 10 kun bor, yo'nalish bo'yicha borish uchun, bir oy ichida biz sizga komissiya natijalarini yuboramiz!",
        
        # Статус
        "status_text": "📊 TEKSHIRUV HOLATI\n\n🆔 Sizning ID: {user_id}\nTashxis: {category}\nBirinchi tashrif sanasi: {registered_at}\nO'tgan kunlar: {days_passed}\nQolgan kunlar: {days_remaining}",
        "no_active_case": "Sizda faol tekshiruvlar yo'q. Boshlash uchun /start tugmasini bosing.",
        "case_stopped": "✅ Eslatmalar to'xtatildi. Qayta boshlash uchun /start tugmasini bosing",
        "expired_status": "⏰ MUDDAT TUGADI\n\n🆔 Sizning ID: {user_id}\nTashxis: {category}\nBirinchi tashrif sanasi: {registered_at}\n\nQo'shimcha tekshiruvlar muddati tugadi. Hujjatlaringiz migratsiya xizmatiga yuborildi.",
        
        # Тексты напоминаний
        "next_reminder_5": "Keyingi eslatma: 5-kun (qolgan {next_reminder} {day_word})",
        "next_reminder_10": "Keyingi eslatma: 10-kun (qolgan {next_reminder} {day_word})",
        "next_reminder_15": "Keyingi eslatma: 15-kun (qolgan {next_reminder} {day_word})",
        "next_reminder_20": "Keyingi eslatma: 20-kun (qolgan {next_reminder} {day_word})",
        "next_reminder_25": "Keyingi eslatma: 25-kun (qolgan {next_reminder} {day_word})",
        "next_reminder_30": "Keyingi eslatma: 30-kun (qolgan {next_reminder} {day_word}) - YAKUNIY",
        "all_reminders_sent": "Barcha eslatmalar yuborildi. Tekshiruv yakunlandi.",
        
        # Сообщения об ошибках
        "error_occurred": "Xatolik yuz berdi. Iltimos, /start tugmasini bosing.",
        "choose_category": "Iltimos, taklif qilingan tugmalardan kategoriyani tanlang.",
        "no_active_examinations": "Sizda faol tekshiruvlar yo'q.",
        "registration_status": "📊 RO'YXATDAN O'TISH HOLATI\n\n🆔 Sizning ID: {user_id}\nRo'yxatdan o'tish sanasi: {registered_at}\nRo'yxatdan o'tishdan beri kunlar: {days_since_registration}\n\nHozircha faol tekshiruvlaringiz yo'q. Boshlash uchun /start tugmasini bosing.",
        
        # Напоминания
        "reminder_template": "⏰ ESLATMA!\n\nTashxis bo'yicha kuzatuv boshlanganidan {days} kun o'tdi: {category}\nMuddat tugashiga qolgan kunlar: {remaining}",
        "final_reminder": (
            "⚠️ DIQQAT!\n\n"
            "Qo'shimcha tekshiruvlar muddati tugadi, hujjatlaringiz migratsiya xizmatiga yuborildi.\n\n"
            "1 kundan keyin botga kirish cheklanadi."
        ),
        "bot_liquidation_message": (
            "🚫 BOT LIQUIDATSIYASI\n\n"
            "Qo'shimcha tekshiruvlar muddati to'liq tugadi.\n"
            "Ma'lumotlaringiz migratsiya xizmatiga uzatildi.\n\n"
            "Botga kirish cheklangan."
        ),
        
        # Переводы типов действий
        "action_bot_started": "Bot ishga tushirildi",
        "action_language_selected": "Til tanlandi",
        "action_button_pressed": "Tugma bosildi",
        "action_diagnosis_chosen": "Tashxis tanlandi",
        "action_examination_result": "Tekshiruv natijasi",
        
        # Переводы данных действий
        "action_data_understood_month": "Oy haqida tushundim",
        "action_data_show_documents": "Hujjatlarni ko'rsatish",
        "action_data_understood_10_days": "10 kun haqida tushundim",
        "action_data_passed_examination": "Tekshiruvni o'tkazdim",
        "action_data_not_passed_examination": "Tekshiruvni o'tkazmadim",
        "action_data_tuberculosis": "Sil kasalligi",
        "action_data_syphilis": "Sifilis",
        "action_data_hiv": "OIV-infektsiya",
        "action_data_drug_addiction": "Giynomaniya",
        "action_data_important_message": "Muhim xabar",
        "action_data_show_diagnosis_menu": "Sizda aniqlandi",
        "action_data_show_help": "Yordam"
    },
    
    "zh": {
        # Выбор языка
        "language_select": "🌍 选择语言:",
        "your_id": "🆔 您的ID: {user_id}",
        "registered_new": "您已注册。",
        "registered_existing": "您已经注册过了。",
        
        # Согласие
        "consent": "要继续使用机器人，需要您同意处理个人数据。\n\n点击下面的按钮继续。",
        "consent_button": "✅ 同意",
        
        # Важное сообщение
        "important_message": "⚠️ 重要消息\n\n您的信息已转交给俄罗斯消费者权益保护局。如果您不完成额外检查，您将收到关于在俄罗斯联邦不受欢迎居留的警告。不要拖延！您有一个月的时间！",
        "understood_month": "✅ 明白，一月",
        
        # Выбор диагноза
        "diagnosis_found": "📋 您被诊断出\n选择您的按钮:",
        "category_select": "选择类别:",
        
        # Диагнозы
        "tuberculosis": "🫁 肺结核",
        "syphilis": "🧬 梅毒", 
        "hiv": "🧫 艾滋病",
        "drug_addiction": "💊 吸毒成瘾",
        
        # Информация о диагнозах (упрощенная версия на китайском)
        "tuberculosis_info": "🫁 肺结核\n\n肺结核是一种极其危险和传染性的疾病，可能导致死亡。它通过空气传播。",
        "syphilis_info": "🧬 梅毒\n\n梅毒是一种通过性传播的危险传染病。可以治疗！",
        "hiv_info": "🧫 艾滋病感染\n\n艾滋病感染是由人类免疫缺陷病毒引起的疾病。",
        "drug_addiction_info": (
            "💊 吸毒成瘾\n\n"
            "您的生物材料已送往地区戒毒所。请记住！阳性结果可能不会得到确认，"
            "所以请不要担心，等待结果。如果结果呈阳性，您最好回家开始治疗，"
            "您也可以联系位于斯塔纽科维奇53号的地区戒毒所来质疑结果。祝您好运！"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 别忘了随身携带:\n• 护照\n• 移民卡\n• 签证\n• 登记",
        "understood_10_days": "✅ 明白，10天",
        "understood_10_days_examination": "明白，10天完成检查",
        "show_documents": "📋 文件",
        "passed_examination": "✅ 完成",
        "not_passed_examination": "❌ 没有",
        "waiting_certificate": "我们在有限责任公司MO«莲花»等待您，地址：符拉迪沃斯托克，斯特列尔科瓦亚街23A",
        
        # Кнопки меню
        "start_button": "🚀 开始",
        "status_button": "📊 状态",
        "help_button": "❓ 帮助",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 打开菜单",
        "cmd_status_desc": "📊 注册状态",
        "cmd_help_desc": "❓ 机器人如何工作？",
        
        # Результат
        "result_received": "✅ 已获得结果",
        "result_received_message": "🎉 太好了！已获得结果。如果需要通过其他检查，请选择类别:",
        
        # Помощь
        "help": "❓ 帮助",
        "help_text": "📚 机器人帮助\n\n命令:\n/start - 开始使用机器人\n/status - 查看注册状态\n/help - 显示此帮助\n\n你有10天时间按指示前往，一个月内我们会发送委员会结果给你！",
        
        # Статус
        "status_text": "📊 检查状态\n\n🆔 您的ID: {user_id}\n诊断: {category}\n首次访问日期: {registered_at}\n已过天数: {days_passed}\n剩余天数: {days_remaining}\n\n{next_reminder_text}",
        "no_active_case": "您没有活跃的检查。按/start开始。",
        "case_stopped": "✅ 提醒已停止。要重新开始，请按/start",
        "expired_status": "⏰ 期限已过\n\n🆔 您的ID: {user_id}\n诊断: {category}\n首次访问日期: {registered_at}\n\n额外检查期限已结束。您的文件已提交给移民服务。",
        
        # Тексты напоминаний
        "next_reminder_5": "下次提醒：第5天（{next_reminder} {day_word}后）",
        "next_reminder_10": "下次提醒：第10天（{next_reminder} {day_word}后）",
        "next_reminder_15": "下次提醒：第15天（{next_reminder} {day_word}后）",
        "next_reminder_20": "下次提醒：第20天（{next_reminder} {day_word}后）",
        "next_reminder_25": "下次提醒：第25天（{next_reminder} {day_word}后）",
        "next_reminder_30": "下次提醒：第30天（{next_reminder} {day_word}后）- 最终",
        "all_reminders_sent": "所有提醒已发送。检查已完成。",
        
        # Сообщения об ошибках
        "error_occurred": "发生错误。请重新按/start。",
        "choose_category": "请从提供的按钮中选择类别。",
        "no_active_examinations": "您没有活跃的检查。",
        "registration_status": "📊 注册状态\n\n🆔 您的ID: {user_id}\n注册日期: {registered_at}\n注册后已过天数: {days_since_registration}\n\n您目前没有活跃的检查。请按/start开始。",
        
        # Напоминания
        "reminder_template": "⏰ 提醒！\n\n诊断观察开始已过{days}天: {category}\n截止日期剩余天数: {remaining}",
        "final_reminder": (
            "⚠️ 注意！\n\n"
            "额外检查期限已结束，您的文件已提交给移民局。\n\n"
            "1天后机器人访问将受限。"
        ),
        "bot_liquidation_message": (
            "🚫 机器人清算\n\n"
            "额外检查期限完全结束。\n"
            "您的数据已转交给移民局。\n\n"
            "机器人访问受限。"
        ),
        
        # Переводы типов действий
        "action_bot_started": "启动机器人",
        "action_language_selected": "选择语言",
        "action_button_pressed": "按下按钮",
        "action_diagnosis_chosen": "选择诊断",
        "action_examination_result": "检查结果",
        
        # Переводы данных действий
        "action_data_understood_month": "理解一个月",
        "action_data_show_documents": "显示文件",
        "action_data_understood_10_days": "理解10天",
        "action_data_passed_examination": "通过检查",
        "action_data_not_passed_examination": "未通过检查",
        "action_data_tuberculosis": "肺结核",
        "action_data_syphilis": "梅毒",
        "action_data_hiv": "艾滋病感染",
        "action_data_drug_addiction": "吸毒成瘾",
        "action_data_important_message": "重要消息",
        "action_data_show_diagnosis_menu": "您被诊断出",
        "action_data_show_help": "帮助"
    },
    
    "ko": {
        # Выбор языка
        "language_select": "🌍 언어 선택:",
        "your_id": "🆔 귀하의 ID: {user_id}",
        "registered_new": "등록되었습니다.",
        "registered_existing": "이미 등록되어 있습니다.",
        
        # Согласие
        "consent": "봇 작업을 계속하려면 개인 데이터 처리에 대한 동의가 필요합니다.\n\n계속하려면 아래 버튼을 클릭하세요.",
        "consent_button": "✅ 동의",
        
        # Важное сообщение
        "important_message": "⚠️ 중요한 메시지\n\n귀하에 대한 정보가 이미 로스포트레브나드조르에 전달되었습니다. 추가 검사를 받지 않으면 러시아 연방에서의 불원하는 체류에 대한 경고를 받게 됩니다. 서두르세요! 한 달이 있습니다!",
        "understood_month": "✅ 이해, 한달",
        
        # Выбор диагноза
        "diagnosis_found": "📋 귀하에게 발견됨\n버튼을 선택하세요:",
        "category_select": "카테고리 선택:",
        
        # Диагнозы
        "tuberculosis": "🫁 결핵",
        "syphilis": "🧬 매독", 
        "hiv": "🧫 HIV",
        "drug_addiction": "💊 마약 중독",
        
        # Информация о диагнозах (упрощенная версия на корейском)
        "tuberculosis_info": "🫁 결핵\n\n결핵은 극도로 위험하고 전염성이 강한 질병으로 사망을 초래할 수 있습니다. 공기로 전파됩니다.",
        "syphilis_info": "🧬 매독\n\n매독은 성적으로 전파되는 위험한 전염병입니다. 치료 가능합니다!",
        "hiv_info": "🧫 HIV 감염\n\nHIV 감염은 인간 면역결핍 바이러스에 의해 발생하는 질병입니다.",
        "drug_addiction_info": (
            "💊 마약 중독\n\n"
            "귀하의 생물학적 재료가 지역 마약학 진료소로 보내졌습니다. 기억하세요! "
            "양성 결과가 확인되지 않을 수 있으므로 걱정하지 말고 결과를 기다리세요. "
            "결과가 양성이라면 집으로 돌아가 치료를 시작하는 것이 좋으며, "
            "결과에 이의를 제기하기 위해 스타뉴코비치 53번지에 있는 지역 마약학 진료소에 연락할 수 있습니다. "
            "행운을 빕니다!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 가져가야 할 것들을 잊지 마세요:\n• 여권\n• 이민 카드\n• 비자\n• 등록",
        "understood_10_days": "✅ 이해, 10일",
        "understood_10_days_examination": "이해, 10일 검사 받기",
        "show_documents": "📋 문서",
        "passed_examination": "✅ 완료",
        "not_passed_examination": "❌ 없음",
        "waiting_certificate": "LLC MO «로토스»에서 증명서와 함께 귀하를 기다립니다. 주소: 블라디보스토크, 스트렐코바야 23A",
        
        # Кнопки 메뉴
        "start_button": "🚀 시작",
        "status_button": "📊 상태",
        "help_button": "❓ 도움말",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 메뉴 열기",
        "cmd_status_desc": "📊 등록 상태",
        "cmd_help_desc": "❓ 봇은 어떻게 작동하나요?",
        
        # Результат
        "result_received": "✅ 결과 수신",
        "result_received_message": "🎉 훌륭합니다! 결과를 받았습니다. 다른 검사가 필요하면 카테고리를 선택하세요:",
        
        # Помощь
        "help": "❓ 도움말",
        "help_text": "📚 봇 도움말\n\n명령어:\n/start - 봇 작업 시작\n/status - 등록 상태 확인\n/help - 이 도움말 표시\n\n지시에 따라 가기 위해 10일이 있으며, 한 달 안에 위원회 결과를 보내드릴 것입니다!",
        
        # Статус
        "status_text": "📊 검사 상태\n\n🆔 귀하의 ID: {user_id}\n진단: {category}\n첫 방문 날짜: {registered_at}\n경과 일수: {days_passed}\n남은 일수: {days_remaining}\n\n{next_reminder_text}",
        "no_active_case": "활성 검사가 없습니다. 시작하려면 /start를 누르세요.",
        "case_stopped": "✅ 알림이 중지되었습니다. 다시 시작하려면 /start를 누르세요",
        "expired_status": "⏰ 기한 만료\n\n🆔 귀하의 ID: {user_id}\n진단: {category}\n첫 방문 날짜: {registered_at}\n\n추가 검사 기한이 종료되었습니다. 귀하의 서류가 이민 서비스에 제출되었습니다.",
        
        # Тексты напоминаний
        "next_reminder_5": "다음 알림: 5일차 ({next_reminder} {day_word} 후)",
        "next_reminder_10": "다음 알림: 10일차 ({next_reminder} {day_word} 후)",
        "next_reminder_15": "다음 알림: 15일차 ({next_reminder} {day_word} 후)",
        "next_reminder_20": "다음 알림: 20일차 ({next_reminder} {day_word} 후)",
        "next_reminder_25": "다음 알림: 25일차 ({next_reminder} {day_word} 후)",
        "next_reminder_30": "다음 알림: 30일차 ({next_reminder} {day_word} 후) - 최종",
        "all_reminders_sent": "모든 알림이 전송되었습니다. 검사가 완료되었습니다.",
        
        # Сообщения об ошибках
        "error_occurred": "오류가 발생했습니다. 다시 /start를 누르세요.",
        "choose_category": "제공된 버튼에서 카테고리를 선택하세요.",
        "no_active_examinations": "활성 검사가 없습니다.",
        "registration_status": "📊 등록 상태\n\n🆔 귀하의 ID: {user_id}\n등록 날짜: {registered_at}\n등록 후 경과 일수: {days_since_registration}\n\n현재 활성 검사가 없습니다. 시작하려면 /start를 누르세요.",
        
        # Напоминания
        "reminder_template": "⏰ 알림!\n\n진단 관찰 시작 후 {days}일 경과: {category}\n마감까지 남은 일수: {remaining}",
        "final_reminder": (
            "⚠️ 주의!\n\n"
            "추가 검사 기간이 종료되었습니다. 귀하의 서류가 이민국에 제출되었습니다.\n\n"
            "1일 후 봇 접근이 제한됩니다."
        ),
        "bot_liquidation_message": (
            "🚫 봇 청산\n\n"
            "추가 검사 기간이 완전히 종료되었습니다.\n"
            "귀하의 데이터가 이민국에 전달되었습니다.\n\n"
            "봇 접근이 제한되었습니다."
        ),
        
        # Переводы типов действий
        "action_bot_started": "봇 시작",
        "action_language_selected": "언어 선택",
        "action_button_pressed": "버튼 누름",
        "action_diagnosis_chosen": "진단 선택",
        "action_examination_result": "검사 결과",
        
        # Переводы данных действий
        "action_data_understood_month": "한 달 이해",
        "action_data_show_documents": "문서 보기",
        "action_data_understood_10_days": "10일 이해",
        "action_data_passed_examination": "검사 통과",
        "action_data_not_passed_examination": "검사 미통과",
        "action_data_tuberculosis": "결핵",
        "action_data_syphilis": "매독",
        "action_data_hiv": "HIV 감염",
        "action_data_drug_addiction": "마약 중독",
        "action_data_important_message": "중요한 메시지",
        "action_data_show_diagnosis_menu": "귀하에게 발견됨",
        "action_data_show_help": "도움말"
    },
    
    "en": {
        # Выбор языка
        "language_select": "🌍 Choose language:",
        "your_id": "🆔 Your ID: {user_id}",
        "registered_new": "You are registered.",
        "registered_existing": "You are already registered.",
        
        # Согласие
        "consent": "To continue working with the bot, your consent to process personal data is required.\n\nClick the button below to continue.",
        "consent_button": "✅ Agree",
        
        # Важное сообщение
        "important_message": "⚠️ IMPORTANT MESSAGE\n\nInformation about you has already been transmitted to ROSPOTREBNADZOR. If you do not undergo additional examinations, you will receive a warning about UNWANTED stay in the Russian Federation. Don't delay! You have one month!",
        "understood_month": "✅ Got it, month",
        
        # Выбор диагноза
        "diagnosis_found": "📋 YOU HAVE BEEN DIAGNOSED\nChoose your button:",
        "category_select": "Choose category:",
        
        # Диагнозы
        "tuberculosis": "🫁 Tuberculosis",
        "syphilis": "🧬 Syphilis", 
        "hiv": "🧫 HIV",
        "drug_addiction": "💊 Drug addiction",
        
        # Информация о диагнозах
        "tuberculosis_info": "🫁 TUBERCULOSIS\n\nTuberculosis is an extremely dangerous and contagious disease that can lead to death. It is transmitted by airborne droplets. With timely diagnosis (Mantoux, Diaskin test, fluorography) it can be cured forever!",
        "syphilis_info": "🧬 SYPHILIS\n\nSyphilis is a dangerous infectious disease transmitted sexually. It can be treated!",
        "hiv_info": "🧫 HIV INFECTION\n\nHIV infection is a disease caused by the human immunodeficiency virus. The virus destroys immune cells that help the body cope with pathogenic microorganisms.",
        "drug_addiction_info": (
            "💊 DRUG ADDICTION\n\n"
            "Your biological material has been sent to the Regional Narcological Dispensary. Remember! "
            "A positive result may not be confirmed, so don't worry, wait for the result. "
            "If the result turns out to be positive, it's better for you to go home and start treatment, "
            "and you can also contact the Regional Narcological Dispensary at Stanjukovich 53 to challenge the result. "
            "All the best!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 Don't forget to bring with you:\n• passport\n• migration card\n• visa\n• registration",
        "understood_10_days": "✅ Got it, 10 days",
        "understood_10_days_examination": "Got it, 10 days examination",
        "show_documents": "📋 Documents",
        "passed_examination": "✅ Done",
        "not_passed_examination": "❌ No",
        "waiting_certificate": "We are waiting for you with a certificate at LLC MO «Lotos» at the address Vladivostok, Strelkovaya 23A",
        
        # Menu buttons
        "start_button": "🚀 Start",
        "status_button": "📊 Status",
        "help_button": "❓ Help",
        
        # Command descriptions for dropdown menu
        "cmd_start_desc": "🚀 Open menu",
        "cmd_status_desc": "📊 Registration status",
        "cmd_help_desc": "❓ How does the bot work?",
        
        # Result
        "result_received": "✅ Result received",
        "result_received_message": "🎉 Great! Result received. If you need to undergo another examination, choose a category:",
        
        # Помощь
        "help": "❓ Help",
        "help_text": "📚 BOT HELP\n\nCommands:\n/start - Start working with the bot\n/status - Find out registration status\n/help - Show this help\n\nYou have 10 days to go by referral, and within a month we will send you the commission results!",
        
        # Статус
        "status_text": "📊 EXAMINATION STATUS\n\n🆔 Your ID: {user_id}\nDiagnosis: {category}\nFirst visit date: {registered_at}\nDays passed: {days_passed}\nDays remaining: {days_remaining}",
        "no_active_case": "You have no active examinations. Press /start to start.",
        "case_stopped": "✅ Reminders stopped. To start again, press /start",
        "expired_status": "⏰ DEADLINE EXPIRED\n\n🆔 Your ID: {user_id}\nDiagnosis: {category}\nFirst visit date: {registered_at}\n\nAdditional examination deadlines have ended. Your documents have been submitted to the migration service.",
        
        # Тексты напоминаний
        "next_reminder_5": "Next reminder: day 5 (in {next_reminder} {day_word})",
        "next_reminder_10": "Next reminder: day 10 (in {next_reminder} {day_word})",
        "next_reminder_15": "Next reminder: day 15 (in {next_reminder} {day_word})",
        "next_reminder_20": "Next reminder: day 20 (in {next_reminder} {day_word})",
        "next_reminder_25": "Next reminder: day 25 (in {next_reminder} {day_word})",
        "next_reminder_30": "Next reminder: day 30 (in {next_reminder} {day_word}) - FINAL",
        "all_reminders_sent": "All reminders sent. Examination completed.",
        
        # Сообщения об ошибках
        "error_occurred": "An error occurred. Please press /start again.",
        "choose_category": "Please choose a category from the provided buttons.",
        "no_active_examinations": "You have no active examinations.",
        "registration_status": "📊 REGISTRATION STATUS\n\n🆔 Your ID: {user_id}\nRegistration date: {registered_at}\nDays since registration: {days_since_registration}\n\nYou currently have no active examinations. Press /start to begin.",
        
        # Напоминания
        "reminder_template": "⏰ REMINDER!\n\n{days} days have passed since the start of observation for diagnosis: {category}\nDays remaining until the deadline: {remaining}",
        "final_reminder": (
            "⚠️ ATTENTION!\n\n"
            "Additional examination deadlines have expired, your documents have been submitted to the migration service.\n\n"
            "Bot access will be restricted in 1 day."
        ),
        "bot_liquidation_message": (
            "🚫 BOT LIQUIDATION\n\n"
            "Additional examination deadlines have completely expired.\n"
            "Your data has been transferred to the migration service.\n\n"
            "Bot access is restricted."
        ),
        
        # Переводы типов действий
        "action_bot_started": "Bot started",
        "action_language_selected": "Language selected",
        "action_button_pressed": "Button pressed",
        "action_diagnosis_chosen": "Diagnosis chosen",
        "action_examination_result": "Examination result",
        
        # Переводы данных действий
        "action_data_understood_month": "Understood month",
        "action_data_show_documents": "Show documents",
        "action_data_understood_10_days": "Understood 10 days",
        "action_data_passed_examination": "Passed examination",
        "action_data_not_passed_examination": "Not passed examination",
        "action_data_tuberculosis": "Tuberculosis",
        "action_data_syphilis": "Syphilis",
        "action_data_hiv": "HIV infection",
        "action_data_drug_addiction": "Drug addiction",
        "action_data_important_message": "Important message",
        "action_data_show_diagnosis_menu": "You have been diagnosed",
        "action_data_show_help": "Help"
    }
}

# Функция для получения текста по языку
def get_text(language: str, key: str, **kwargs) -> str:
    """Получить текст по языку и ключу"""
    if language not in TEXTS:
        language = "ru"  # По умолчанию русский
    
    if key not in TEXTS[language]:
        # Если текста нет на выбранном языке, берем русский
        if key in TEXTS["ru"]:
            return TEXTS["ru"][key].format(**kwargs)
        return f"Text not found: {key}"
    
    return TEXTS[language][key].format(**kwargs)

# Старые константы для совместимости (будут удалены)
CONSENT_TEXT = TEXTS["ru"]["consent"]
CONSENT_BUTTON_TEXT = TEXTS["ru"]["consent_button"]
CATEGORY_SELECT_TEXT = TEXTS["ru"]["category_select"]
RESULT_RECEIVED_TEXT = TEXTS["ru"]["result_received"]
RESULT_RECEIVED_MESSAGE = TEXTS["ru"]["result_received_message"]

BUTTONS = {
    "Туберкулез": TEXTS["ru"]["tuberculosis"],
    "Сифилис": TEXTS["ru"]["syphilis"],
    "ВИЧ-инфекция": TEXTS["ru"]["hiv"],
    "Наркомания": TEXTS["ru"]["drug_addiction"],
}

INFO_TEXTS = {
    "Туберкулез": TEXTS["ru"]["tuberculosis_info"],
    "Сифилис": TEXTS["ru"]["syphilis_info"],
    "ВИЧ-инфекция": TEXTS["ru"]["hiv_info"],
    "Наркомания": TEXTS["ru"]["drug_addiction_info"],
}

HELP_TEXT = TEXTS["ru"]["help_text"]
STATUS_TEXT = TEXTS["ru"]["status_text"]
NO_ACTIVE_CASE = TEXTS["ru"]["no_active_case"]
CASE_STOPPED = TEXTS["ru"]["case_stopped"]
REMINDER_TEMPLATE = TEXTS["ru"]["reminder_template"]
FINAL_REMINDER = TEXTS["ru"]["final_reminder"]

