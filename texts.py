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
        
        # Выбор языка
        "language_selection": "Выберите язык:",
        "registration_info": """👤 ID пользователя: {user_id}
📅 {registration_status}
🕐 Дата регистрации: {registration_date}

Выберите язык:""",
        
        # Важное сообщение
        "important_message": "⚠️ ВАЖНОЕ СООБЩЕНИЕ\n\nПо Вам уже передали сведения в РОСПОТРЕБНАДЗОР. Если Вы не пройдете дообследования, Вы получите представление о НЕЖЕЛАТЕЛЬНОМ пребывании в Российской Федерации. Не медлите! У Вас есть один месяц!",
        "understood_month": "✅ Понял",
        "understood_examination": "✅ Понял",
        
        # Выбор диагноза
        "diagnosis_found": "📋 Вам необходимо пройти дообследование",
        "category_select": "📋 У вас выявлено заболевание. Пожалуйста, выберите из списка:",
        
        # Диагнозы
        "tuberculosis": "🫁 Туберкулёз",
        "syphilis": "🧬 Сифилис", 
        "hiv": "🧫 ВИЧ",
        "drug_addiction": "💊 Наркомания",
        
        # Информация о диагнозах
        "tuberculosis_info": (
            "🫁 ТУБЕРКУЛЁЗ\n\n"
            "Туберкулёз — опасное и заразное заболевание, которое при отсутствии лечения может привести к смерти. Он передаётся воздушно-капельным путём, поэтому важно вовремя пройти обследование. При своевременной диагностике (пробы Манту, Диаскинтест, флюорография) туберкулёз полностью излечим. Не переживайте и как можно скорее обратитесь в Противотуберкулёзный диспансер с нашим направлением — ГБУЗ ПКПТД по адресу: Владивосток, ул. 4-я Флотская, 37/39. У вас есть 10 дней, чтобы посетить врача-фтизиатра. При необходимости врач может назначить посев мокроты и компьютерную томографию органов грудной клетки."
        ),
        "syphilis_info": (
            "🧬 СИФИЛИС\n\n"
            "Сифилис — опасное инфекционное заболевание, передающееся преимущественно половым путём. Оно поддаётся лечению, особенно при своевременном обращении к врачу. Не переживайте и как можно скорее обратитесь в Кожно-венерологический диспансер с нашим направлением — ГБУЗ ККВД, по адресу: г. Владивосток, ул. Гамарника, 18В. У вас есть 10 дней, чтобы посетить врача-дерматовенеролога."
        ),
        "hiv_info": (
            "🧫 ВИЧ-ИНФЕКЦИЯ\n\n"
            "ВИЧ-инфекция — это заболевание, вызываемое вирусом иммунодефицита человека (ВИЧ). Этот вирус поражает и уничтожает клетки иммунной системы, которые защищают организм от инфекций.\n\n"
            "Современная антиретровирусная терапия (АРВТ) позволяет подавлять размножение вируса и значительно продлевает жизнь пациентов. Однако в России лечение данными препаратами по юридическим причинам недоступно.\n\n"
            "Для получения консультации обратитесь в Краевую клиническую больницу № 2, Центр по профилактике и борьбе со СПИД и инфекционными заболеваниями, по адресу: г. Владивосток, ул. Босисенко, 50."
        ),
        "drug_addiction_info": (
            "💊 НАРКОМАНИЯ\n\n"
            "Ваш биологический материал направлен в Краевой наркологический диспансер. Помните: положительный результат может не подтвердиться, поэтому не переживайте — дождитесь окончательного заключения. Если результат всё же окажется положительным, рекомендуется вернуться домой и начать лечение. Также вы можете обратиться в Краевой наркологический диспансер по адресу: г. Владивосток, ул. Станюковича, 53, чтобы при необходимости оспорить результат анализа. Всего вам наилучшего и крепкого здоровья!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 Не забудьте с собой взять:\n• паспорт\n• миграционная карта\n• виза\n• регистрация",
        "understood_10_days": "✅ Понял",
        "understood_10_days_examination": "Понял, 10 дней",
        "show_documents": "📋 Документы",
        "examination_question": "Вы прошли дообследование?",
        "passed_examination": "✅ Да",
        "not_passed_examination": "❌ Нет",
        "waiting_certificate": "Ждем Вас со справкой в ООО МО «Лотос» по адресу Владивосток, Стрелковая 23А",
        "examination_completed": "✅ Отлично! Обследование пройдено успешно.",
        "examination_required": "⚠️ Необходимо пройти обследование в течение 10 дней.",
        "not_passed_message": "❌ Вы не прошли обследование. Необходимо пройти повторно.",
        
        # Статус
        "status_examination": """📊 СТАТУС ОБСЛЕДОВАНИЯ

👤 ID пользователя: {user_id}
📅 Дата регистрации в боте: {registration_date}
🩺 Дата выбора диагноза: {diagnosis_date}
⏰ Срок окончания: {deadline_date}
📆 {days_text}

⚠️ Необходимо пройти обследование в течение 10 дней с выбора диагноза.""",
        
        "status_registration": """📊 СТАТУС РЕГИСТРАЦИИ

👤 ID пользователя: {user_id}
📅 Дата регистрации в боте: {registration_date}
🩺 Статус: Ожидание выбора диагноза

Выберите диагноз для начала процесса обследования.""",
        
        "days_left": "Осталось дней: {days}",
        "last_day": "Последний день!",
        "overdue": "Просрочено на {days} дней",
        
        # Статусы регистрации
        "already_registered": "Вы уже зарегистрированы",
        "just_registered": "Вы зарегистрировались",
        "user_id": "ID пользователя",
        "registration_date": "Дата регистрации",
        "diagnosis_date": "Дата выбора диагноза",
        "deadline_date": "Срок окончания",
        "status": "Статус",
        "waiting_diagnosis": "Ожидание выбора диагноза",
        "choose_diagnosis": "Выберите диагноз для начала процесса обследования",
        "click_for_status": "Нажмите кнопку для просмотра статуса:",
        "click_for_help": "Нажмите кнопку для просмотра справки:",
        "show_status": "📊 Показать статус",
        "show_help": "❓ Показать справку",
        
        # Ошибки
        "invalid_selection": "❌ Неверный выбор. Пожалуйста, выберите один из предложенных вариантов.",
        
        # Кнопки меню
        "start_button": "🚀 Старт",
        "status_button": "📊 Статус",
        "help_button": "❓ Помощь",
        "main_menu_text": "Выберите действие:",
        
        # Команды бота
        "start_command": "🆔 ID пользователя: {user_id}\n📅 Дата регистрации: {registration_date}\n✅ {registration_status}\n⏰ Осталось дней: {days_left}\n\n🌍 Выберите язык:",
        "status_command": "📊 Статус регистрации",
        "help_command": "❓ Справка по командам",
        
        # Описания команд для выпадающего меню
        "start_cmd_desc": "🚀 Открыть меню",
        "status_cmd_desc": "📊 Статус регистрации", 
        "help_cmd_desc": "❓ Как работает бот?",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 Открыть меню",
        "cmd_status_desc": "📊 Статус регистрации", 
        "cmd_help_desc": "❓ Как работает бот?",
        
        # Результат
        
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
        "no_active_case": "У тебя нет активных обследований. Нажми /start, чтобы начать.",
        
        # Финальные уведомления
    "final_reminder": "⚠️ ВНИМАНИЕ! Сроки по дообследованию закончены, Ваши документы поданы в миграционную службу.",
    "bot_liquidation_message": "🚫 Ваш доступ к боту завершен. Сроки по дообследованию истекли.",
    "regular_reminder": "⏰ Напоминание: прошло {days_passed}",
        
        
        # Сообщения об ошибках
        "error_occurred": "Произошла ошибка. Пожалуйста, нажмите /start заново.",
        "choose_category": "Пожалуйста, выберите категорию из предложенных кнопок.",
        "examination_reminder": "✅ Спасибо за выбор! Теперь вам необходимо пройти обследование в течение 30 дней с момента регистрации.",
        "no_active_examinations": "У Вас нет активных обследований.",
        "registration_status": "📊 СТАТУС РЕГИСТРАЦИИ\n\n🆔 Ваш ID: {user_id}\nДата регистрации: {registered_at}\nПрошло дней с регистрации: {days_since_registration}\n\nУ Вас пока нет активных обследований. Нажмите /start для начала.",
        
        
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
        
        # Выбор языка
        "language_selection": "Tilni tanlang:",
        "registration_info": """👤 Foydalanuvchi ID: {user_id}
📅 {registration_status}
🕐 Ro'yxatdan o'tish sanasi: {registration_date}

Tilni tanlang:""",
        
        # Важное сообщение
        "important_message": "⚠️ MUHIM XABAR\n\nSiz haqingizda ma'lumotlar ROSPOTREBNADZORga uzatilgan. Agar siz qo'shimcha tekshiruvlarni o'tkazmasangiz, Rossiya Federatsiyasida istalmagan qolish haqida ta'kidnoma olasiz. Shoshiling! Sizda bir oy bor!",
        "understood_month": "✅ Tushundim",
        "understood_examination": "✅ Tushundim",
        
        # Выбор диагноза
        "diagnosis_found": "📋 Sizga qo'shimcha tekshiruv kerak",
        "category_select": "📋 Sizda kasallik aniqlandi. Iltimos, ro'yxatdan tanlang:",
        
        # Диагнозы
        "tuberculosis": "🫁 Sil kasalligi",
        "syphilis": "🧬 Sifilis", 
        "hiv": "🧫 OIV",
        "drug_addiction": "💊 Giynomaniya",
        
        # Информация о диагнозах (упрощенная версия на узбекском)
        "tuberculosis_info": (
            "🫁 SIL KASALLIGI\n\n"
            "Sil kasalligi - xavfli va yuqumli kasallik bo'lib, davolanmasa o'limga olib kelishi mumkin. U havo orqali yuqadi, shuning uchun vaqtida tekshiruvdan o'tish muhimdir. Vaqtida tashxis qo'yilsa (Mantu, Diaskin-test, flyuorografiya) sil butunlay davolash mumkin. Tashvishlanmang va bizning yo'naltiruvchi bilan imkon qadar tezroq Silga qarshi kurashish dispanserga murojaat qiling - GBUZ PKPTD manzili: Vladivostok, 4-Flot ko'chasi, 37/39. Sizda shifokor-fiziaterga borish uchun 10 kun vaqtingiz bor. Kerak bo'lsa, shifokor balg'am ekish va ko'krak qafasi a'zolarining kompyuter tomografiyasini buyurishi mumkin."
        ),
        "syphilis_info": (
            "🧬 SIFILIS\n\n"
            "Sifilis - asosan jinsiy yo'l bilan yuqadigan xavfli yuqumli kasallik. U davolash mumkin, ayniqsa shifokorga vaqtida murojaat qilganda. Tashvishlanmang va bizning yo'naltiruvchi bilan imkon qadar tezroq Teri-venerologik dispanserga murojaat qiling - GBUZ KKVVD, manzili: Vladivostok sh., Gamarnika ko'chasi, 18V. Sizda teri-venerolog shifokoriga borish uchun 10 kun vaqtingiz bor."
        ),
        "hiv_info": (
            "🧫 OIV-INFECTSIYA\n\n"
            "OIV-infektsiya - bu inson immunitet tanqisligi virusi (OIV) tufayli yuzaga keladigan kasallik. Bu virus immunitet tizimining hujayralarini zararlaydi va yo'q qiladi, ular organizmni infektsiyalardan himoya qiladi.\n\n"
            "Zamonaviy antiretrovirus terapiyasi (ART) virusning ko'payishini bostirishga va bemorlarning hayotini sezilarli darajada uzaytirishga imkon beradi. Biroq, Rossiyada bu dorilar bilan davolash huquqiy sabablarga ko'ra mavjud emas.\n\n"
            "Maslahat olish uchun Viloyat klinik kasalxonasi № 2, OIV va yuqumli kasalliklarni oldini olish va kurashish markaziga murojaat qiling, manzili: Vladivostok sh., Bosisenko ko'chasi, 50."
        ),
        "drug_addiction_info": (
            "💊 GIYNOMANIYA\n\n"
            "Sizning biologik materialingiz Viloyat narkologik dispanseriga yuborildi. Eslab qoling: ijobiy natija tasdiqlanmasligi mumkin, shuning uchun tashvishlanmang — yakuniy xulosani kutib turing. Agar natija baribir ijobiy bo'lsa, uyga qaytib, davolanishni boshlash tavsiya etiladi. Shuningdek, kerak bo'lsa, tahlil natijasini rad etish uchun Viloyat narkologik dispanserga murojaat qilishingiz mumkin, manzili: Vladivostok sh., Stanyukovich ko'chasi, 53. Sizga eng yaxshi va mustahkam salomatlik tilaymiz!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 O'zingiz bilan olib kelishni unutmang:\n• pasport\n• migratsiya karta\n• viza\n• ro'yxatdan o'tish",
        "understood_10_days": "✅ Tushundim",
        "understood_10_days_examination": "Tushundim, 10 kun",
        "show_documents": "📋 Hujjatlar",
        "examination_question": "Siz qo'shimcha tekshiruvni o'tkazingizmi?",
        "passed_examination": "✅ Ha",
        "not_passed_examination": "❌ Yo'q",
        "waiting_certificate": "Sizni OOO MO «Lotos»da, Vladivostok, Strelkovaya 23A manzilida spravka bilan kutamiz",
        "examination_completed": "✅ Ajoyib! Tekshiruv muvaffaqiyatli o'tkazildi.",
        "examination_required": "⚠️ 10 kun ichida tekshiruvni o'tkazish kerak.",
        "not_passed_message": "❌ Siz tekshiruvni o'tkazmadingiz. Qaytadan o'tkazish kerak.",
        
        # Статусы регистрации
        "already_registered": "Siz allaqachon ro'yxatdan o'tgansiz",
        "just_registered": "Siz ro'yxatdan o'tdingiz",
        "user_id": "Foydalanuvchi ID",
        "registration_date": "Ro'yxatdan o'tish sanasi",
        "diagnosis_date": "Tashxis tanlash sanasi",
        "deadline_date": "Tugash sanasi",
        "status": "Holat",
        "waiting_diagnosis": "Tashxis tanlashni kutish",
        "choose_diagnosis": "Tekshiruv jarayonini boshlash uchun tashxisni tanlang",
        "click_for_status": "Holatni ko'rish uchun tugmani bosing:",
        "click_for_help": "Yordamni ko'rish uchun tugmani bosing:",
        "show_status": "📊 Holatni ko'rsatish",
        "show_help": "❓ Yordamni ko'rsatish",
        
        # Ошибки
        "invalid_selection": "❌ Noto'g'ri tanlov. Iltimos, taklif qilingan variantlardan birini tanlang.",
        
        # Кнопки меню
        "start_button": "🚀 Boshlash",
        "status_button": "📊 Holat",
        "help_button": "❓ Yordam",
        "main_menu_text": "Amalni tanlang:",
        
        # Команды бота
        "start_command": "🆔 Foydalanuvchi ID: {user_id}\n📅 Ro'yxatdan o'tish sanasi: {registration_date}\n✅ {registration_status}\n⏰ Qolgan kunlar: {days_left}\n\n🌍 Tilni tanlang:",
        "status_command": "📊 Ro'yxatdan o'tish holati",
        "help_command": "❓ Buyruqlar haqida ma'lumot",
        
        # Описания команд для выпадающего меню
        "start_cmd_desc": "🚀 Menyuni ochish",
        "status_cmd_desc": "📊 Ro'yxatdan o'tish holati",
        "help_cmd_desc": "❓ Bot qanday ishlaydi?",
        
        # Статусы времени
        "days_left": "Qolgan kunlar: {days}",
        "last_day": "Oxirgi kun!",
        "overdue": "Muddati o'tgan: {days} kun",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 Menyuni ochish",
        "cmd_status_desc": "📊 Ro'yxatdan o'tish holati",
        "cmd_help_desc": "❓ Bot qanday ishlaydi?",
        
        # Результат
        
        # Помощь
        "help": "❓ Yordam",
        "help_text": "📚 BOT HAQIDA MA'LUMOT\n\nBuyruqlar:\n/start - Bot bilan ishlashni boshlash\n/status - Ro'yxatdan o'tish holatini bilish\n/help - Bu yordamni ko'rsatish\n\nSizda 10 kun bor, yo'nalish bo'yicha borish uchun, bir oy ichida biz sizga komissiya natijalarini yuboramiz!",
        
        # Статус
        "no_active_case": "Sizda faol tekshiruvlar yo'q. Boshlash uchun /start tugmasini bosing.",
        
        # Финальные уведомления
        
        
        # Сообщения об ошибках
        "error_occurred": "Xatolik yuz berdi. Iltimos, /start tugmasini bosing.",
        "choose_category": "Iltimos, taklif qilingan tugmalardan kategoriyani tanlang.",
        "examination_reminder": "✅ Tanlov uchun rahmat! Endi siz ro'yxatdan o'tgan kundan boshlab 30 kun ichida tekshiruvdan o'tishingiz kerak.",
        "no_active_examinations": "Sizda faol tekshiruvlar yo'q.",
        "registration_status": "📊 RO'YXATDAN O'TISH HOLATI\n\n🆔 Sizning ID: {user_id}\nRo'yxatdan o'tish sanasi: {registered_at}\nRo'yxatdan o'tishdan beri kunlar: {days_since_registration}\n\nHozircha faol tekshiruvlaringiz yo'q. Boshlash uchun /start tugmasini bosing.",
        
        # Напоминания
        
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
        "action_data_show_help": "Yordam",
        
        # Напоминания
        "regular_reminder": "⏰ Eslatma: {days_passed} o'tdi",
        "final_reminder": "⚠️ EHTIYOT! Qo'shimcha tekshiruv muddati tugadi, hujjatlaringiz migratsiya xizmatiga taqdim etildi.",
        "bot_liquidation_message": "🚫 Bot bilan ishlash muddati tugadi. Qo'shimcha tekshiruv muddati o'tdi."
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
        
        # Выбор языка
        "language_selection": "选择语言:",
        "registration_info": """👤 用户ID: {user_id}
📅 {registration_status}
🕐 注册日期: {registration_date}

选择语言:""",
        
        # Важное сообщение
        "important_message": "⚠️ 重要消息\n\n您的信息已转交给俄罗斯消费者权益保护局。如果您不完成额外检查，您将收到关于在俄罗斯联邦不受欢迎居留的警告。不要拖延！您有一个月的时间！",
        "understood_month": "✅ 明白",
        "understood_examination": "✅ 明白",
        
        # Выбор диагноза
        "diagnosis_found": "📋 您需要进行额外检查",
        "category_select": "📋 您被诊断出疾病。请从列表中选择:",
        
        # Диагнозы
        "tuberculosis": "🫁 肺结核",
        "syphilis": "🧬 梅毒", 
        "hiv": "🧫 艾滋病",
        "drug_addiction": "💊 吸毒成瘾",
        
        # Информация о диагнозах (упрощенная версия на китайском)
        "tuberculosis_info": (
            "🫁 肺结核\n\n"
            "肺结核是一种危险且传染性的疾病，如果不治疗可能导致死亡。它通过空气传播，因此及时检查很重要。及时诊断（曼图试验、迪阿斯金试验、X光检查）可以完全治愈肺结核。请不要担心，请尽快携带我们的转诊单前往结核病防治所——GBUZ PKPTD，地址：符拉迪沃斯托克，4-я弗洛茨卡亚街37/39号。您有10天时间去看肺科医生。如有必要，医生可能会要求进行痰培养和胸部器官计算机断层扫描。"
        ),
        "syphilis_info": (
            "🧬 梅毒\n\n"
            "梅毒是一种危险传染病，主要通过性传播。它可以治疗，特别是及时就医时。请不要担心，请尽快携带我们的转诊单前往皮肤性病防治所——GBUZ KKVVD，地址：符拉迪沃斯托克市，加马尔尼卡街18V号。您有10天时间去看皮肤性病医生。"
        ),
        "hiv_info": (
            "🧫 艾滋病感染\n\n"
            "艾滋病感染是由人类免疫缺陷病毒（HIV）引起的疾病。这种病毒攻击并破坏免疫系统的细胞，这些细胞保护身体免受感染。\n\n"
            "现代抗逆转录病毒疗法（ART）可以抑制病毒复制并显著延长患者生命。然而，在俄罗斯，由于法律原因，无法使用这些药物治疗。\n\n"
            "如需咨询，请联系边疆区临床医院第2号，艾滋病和传染病预防控制中心，地址：符拉迪沃斯托克市，博里森科街50号。"
        ),
        "drug_addiction_info": (
            "💊 吸毒成瘾\n\n"
            "您的生物材料已送往地区戒毒所。请记住：阳性结果可能不会得到确认，所以请不要担心——请等待最终结论。如果结果确实呈阳性，建议您回家开始治疗。您也可以联系地区戒毒所，地址：符拉迪沃斯托克市，斯塔纽科维奇街53号，以便在必要时质疑分析结果。祝您一切顺利，身体健康！"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 别忘了随身携带:\n• 护照\n• 移民卡\n• 签证\n• 登记",
        "understood_10_days": "✅ 明白",
        "understood_10_days_examination": "明白，10天",
        "show_documents": "📋 文件",
        "examination_question": "您是否完成了额外检查？",
        "passed_examination": "✅ 是",
        "not_passed_examination": "❌ 没有",
        "waiting_certificate": "我们在有限责任公司MO«莲花»等待您，地址：符拉迪沃斯托克，斯特列尔科瓦亚街23A",
        "examination_completed": "✅ 太好了！检查成功完成。",
        "examination_required": "⚠️ 需要在10天内完成检查。",
        "not_passed_message": "❌ 您没有完成检查。需要重新完成。",
        
        # Статусы регистрации
        "already_registered": "您已经注册",
        "just_registered": "您已注册",
        "user_id": "用户ID",
        "registration_date": "注册日期",
        "diagnosis_date": "诊断选择日期",
        "deadline_date": "截止日期",
        "status": "状态",
        "waiting_diagnosis": "等待选择诊断",
        "choose_diagnosis": "请选择诊断以开始检查过程",
        "click_for_status": "点击按钮查看状态：",
        "click_for_help": "点击按钮查看帮助：",
        "show_status": "📊 显示状态",
        "show_help": "❓ 显示帮助",
        
        # Ошибки
        "invalid_selection": "❌ 选择无效。请从提供的选项中选择一个。",
        
        # Кнопки меню
        "start_button": "🚀 开始",
        "status_button": "📊 状态",
        "help_button": "❓ 帮助",
        "main_menu_text": "请选择操作:",
        
        # Команды бота
        "start_command": "🆔 用户ID: {user_id}\n📅 注册日期: {registration_date}\n✅ {registration_status}\n⏰ 剩余天数: {days_left}\n\n🌍 选择语言:",
        "status_command": "📊 注册状态",
        "help_command": "❓ 命令帮助",
        
        # Описания команд для выпадающего меню
        "start_cmd_desc": "🚀 打开菜单",
        "status_cmd_desc": "📊 注册状态",
        "help_cmd_desc": "❓ 机器人如何工作？",
        
        # Статусы времени
        "days_left": "剩余天数: {days}",
        "last_day": "最后一天！",
        "overdue": "已逾期 {days} 天",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 打开菜单",
        "cmd_status_desc": "📊 注册状态",
        "cmd_help_desc": "❓ 机器人如何工作？",
        
        # Результат
        
        # Помощь
        "help": "❓ 帮助",
        "help_text": "📚 机器人帮助\n\n命令:\n/start - 开始使用机器人\n/status - 查看注册状态\n/help - 显示此帮助\n\n你有10天时间按指示前往，一个月内我们会发送委员会结果给你！",
        
        # Статус
        "no_active_case": "您没有活跃的检查。按/start开始。",
        
        # Финальные уведомления
        
        
        # Сообщения об ошибках
        "error_occurred": "发生错误。请重新按/start。",
        "choose_category": "请从提供的按钮中选择类别。",
        "examination_reminder": "✅ 感谢您的选择！现在您需要在注册之日起30天内接受检查。",
        "no_active_examinations": "您没有活跃的检查。",
        "registration_status": "📊 注册状态\n\n🆔 您的ID: {user_id}\n注册日期: {registered_at}\n注册后已过天数: {days_since_registration}\n\n您目前没有活跃的检查。请按/start开始。",
        
        # Напоминания
        
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
        "action_data_show_help": "帮助",
        
        # Напоминания
        "regular_reminder": "⏰ 提醒：已过 {days_passed}",
        "final_reminder": "⚠️ 注意！额外检查期限已结束，您的文件已提交给移民局。",
        "bot_liquidation_message": "🚫 您的机器人访问已结束。额外检查期限已过期。"
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
        
        # Выбор языка
        "language_selection": "언어 선택:",
        "registration_info": """👤 사용자 ID: {user_id}
📅 {registration_status}
🕐 등록 날짜: {registration_date}

언어 선택:""",
        
        # Важное сообщение
        "important_message": "⚠️ 중요한 메시지\n\n귀하에 대한 정보가 이미 로스포트레브나드조르에 전달되었습니다. 추가 검사를 받지 않으면 러시아 연방에서의 불원하는 체류에 대한 경고를 받게 됩니다. 서두르세요! 한 달이 있습니다!",
        "understood_month": "✅ 이해",
        "understood_examination": "✅ 이해",
        
        # Выбор диагноза
        "diagnosis_found": "📋 추가 검사가 필요합니다",
        "category_select": "📋 귀하에게 질병이 발견되었습니다. 목록에서 선택해 주세요:",
        
        # Диагнозы
        "tuberculosis": "🫁 결핵",
        "syphilis": "🧬 매독", 
        "hiv": "🧫 HIV",
        "drug_addiction": "💊 마약 중독",
        
        # Информация о диагнозах (упрощенная версия на корейском)
        "tuberculosis_info": (
            "🫁 결핵\n\n"
            "결핵은 치료하지 않으면 사망에 이를 수 있는 위험하고 전염성이 강한 질병입니다. 공기를 통해 전파되므로 적시에 검사를 받는 것이 중요합니다. 적시 진단(만투, 디아스킨 테스트, X선 검사)으로 결핵을 완전히 치료할 수 있습니다. 걱정하지 마시고 가능한 한 빨리 우리의 추천서를 가지고 결핵 예방 센터에 연락하세요 - GBUZ PKPTD 주소: 블라디보스토크, 4-ya 플로츠카야 거리 37/39. 폐과 의사를 방문할 10일의 시간이 있습니다. 필요시 의사는 가래 배양 검사와 흉부 기관의 컴퓨터 단층 촬영을 처방할 수 있습니다."
        ),
        "syphilis_info": (
            "🧬 매독\n\n"
            "매독은 주로 성적으로 전파되는 위험한 전염병입니다. 치료가 가능하며, 특히 적시에 의사를 방문할 때 더욱 그렇습니다. 걱정하지 마시고 가능한 한 빨리 우리의 추천서를 가지고 피부과 성병 진료소에 연락하세요 - GBUZ KKVVD, 주소: 블라디보스토크시, 가마르니카 거리 18V. 피부과 성병 의사를 방문할 10일의 시간이 있습니다."
        ),
        "hiv_info": (
            "🧫 HIV 감염\n\n"
            "HIV 감염은 인간 면역결핍 바이러스(HIV)에 의해 발생하는 질병입니다. 이 바이러스는 감염으로부터 신체를 보호하는 면역 시스템의 세포를 공격하고 파괴합니다.\n\n"
            "현대 항레트로바이러스 요법(ART)은 바이러스 복제를 억제하고 환자의 생명을 크게 연장할 수 있습니다. 그러나 러시아에서는 법적 이유로 이러한 약물로 치료할 수 없습니다.\n\n"
            "상담을 위해서는 지역 임상 병원 제2호, AIDS 및 전염병 예방 및 치료 센터에 연락하세요. 주소: 블라디보스토크시, 보리센코 거리 50."
        ),
        "drug_addiction_info": (
            "💊 마약 중독\n\n"
            "귀하의 생물학적 재료가 지역 마약학 진료소로 보내졌습니다. 기억하세요: 양성 결과가 확인되지 않을 수 있으므로 걱정하지 말고 최종 결론을 기다리세요. 결과가 정말로 양성이라면 집으로 돌아가 치료를 시작하는 것이 좋습니다. 또한 필요시 분석 결과에 이의를 제기하기 위해 지역 마약학 진료소에 연락할 수 있습니다. 주소: 블라디보스토크시, 스타뉴코비치 거리 53. 최선을 다하고 건강하시길 바랍니다!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 가져가야 할 것들을 잊지 마세요:\n• 여권\n• 이민 카드\n• 비자\n• 등록",
        "understood_10_days": "✅ 이해",
        "understood_10_days_examination": "이해, 10일",
        "show_documents": "📋 문서",
        "examination_question": "추가 검사를 받으셨나요?",
        "passed_examination": "✅ 예",
        "not_passed_examination": "❌ 아니오",
        "waiting_certificate": "LLC MO «로토스»에서 증명서와 함께 귀하를 기다립니다. 주소: 블라디보스토크, 스트렐코바야 23A",
        "examination_completed": "✅ 훌륭합니다! 검사가 성공적으로 완료되었습니다.",
        "examination_required": "⚠️ 10일 내에 검사를 받아야 합니다.",
        "not_passed_message": "❌ 검사를 받지 않았습니다. 다시 받아야 합니다.",
        
        # Статусы регистрации
        "already_registered": "이미 등록되었습니다",
        "just_registered": "등록되었습니다",
        "user_id": "사용자 ID",
        "registration_date": "등록 날짜",
        "diagnosis_date": "진단 선택 날짜",
        "deadline_date": "마감 날짜",
        "status": "상태",
        "waiting_diagnosis": "진단 선택 대기",
        "choose_diagnosis": "검사 과정을 시작하려면 진단을 선택하세요",
        "click_for_status": "상태를 보려면 버튼을 클릭하세요:",
        "click_for_help": "도움말을 보려면 버튼을 클릭하세요:",
        "show_status": "📊 상태 표시",
        "show_help": "❓ 도움말 표시",
        
        # Ошибки
        "invalid_selection": "❌ 잘못된 선택입니다. 제공된 옵션 중 하나를 선택해 주세요.",
        
        # Кнопки 메뉴
        "start_button": "🚀 시작",
        "status_button": "📊 상태",
        "help_button": "❓ 도움말",
        "main_menu_text": "작업을 선택하세요:",
        
        # Команды бота
        "start_command": "🆔 사용자 ID: {user_id}\n📅 등록 날짜: {registration_date}\n✅ {registration_status}\n⏰ 남은 일수: {days_left}\n\n🌍 언어를 선택하세요:",
        "status_command": "📊 등록 상태",
        "help_command": "❓ 명령어 도움말",
        
        # Описания команд для выпадающего меню
        "start_cmd_desc": "🚀 메뉴 열기",
        "status_cmd_desc": "📊 등록 상태",
        "help_cmd_desc": "❓ 봇은 어떻게 작동하나요?",
        
        # Статусы времени
        "days_left": "남은 일수: {days}",
        "last_day": "마지막 날!",
        "overdue": "기한 초과 {days}일",
        
        # Описания команд для выпадающего меню
        "cmd_start_desc": "🚀 메뉴 열기",
        "cmd_status_desc": "📊 등록 상태",
        "cmd_help_desc": "❓ 봇은 어떻게 작동하나요?",
        
        # Результат
        
        # Помощь
        "help": "❓ 도움말",
        "help_text": "📚 봇 도움말\n\n명령어:\n/start - 봇 작업 시작\n/status - 등록 상태 확인\n/help - 이 도움말 표시\n\n지시에 따라 가기 위해 10일이 있으며, 한 달 안에 위원회 결과를 보내드릴 것입니다!",
        
        # Статус
        "no_active_case": "활성 검사가 없습니다. 시작하려면 /start를 누르세요.",
        
        # Финальные уведомления
        
        
        # Сообщения об ошибках
        "error_occurred": "오류가 발생했습니다. 다시 /start를 누르세요.",
        "choose_category": "제공된 버튼에서 카테고리를 선택하세요.",
        "examination_reminder": "✅ 선택해 주셔서 감사합니다! 이제 등록일로부터 30일 이내에 검사를 받으셔야 합니다.",
        "no_active_examinations": "활성 검사가 없습니다.",
        "registration_status": "📊 등록 상태\n\n🆔 귀하의 ID: {user_id}\n등록 날짜: {registered_at}\n등록 후 경과 일수: {days_since_registration}\n\n현재 활성 검사가 없습니다. 시작하려면 /start를 누르세요.",
        
        # Напоминания
        
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
        "action_data_show_help": "도움말",
        
        # Напоминания
        "regular_reminder": "⏰ 알림: {days_passed} 경과",
        "final_reminder": "⚠️ 주의! 추가 검사 기한이 종료되었습니다. 귀하의 서류가 이민국에 제출되었습니다.",
        "bot_liquidation_message": "🚫 귀하의 봇 액세스가 종료되었습니다. 추가 검사 기한이 만료되었습니다."
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
        
        # Выбор языка
        "language_selection": "Choose language:",
        "registration_info": """👤 User ID: {user_id}
📅 {registration_status}
🕐 Registration date: {registration_date}

Choose language:""",
        
        # Важное сообщение
        "important_message": "⚠️ IMPORTANT MESSAGE\n\nInformation about you has already been transmitted to ROSPOTREBNADZOR. If you do not undergo additional examinations, you will receive a warning about UNWANTED stay in the Russian Federation. Don't delay! You have one month!",
        "understood_month": "✅ Got it",
        "understood_examination": "✅ Got it",
        
        # Выбор диагноза
        "diagnosis_found": "📋 You need to undergo additional examination",
        "category_select": "📋 You have been diagnosed with a disease. Please choose from the list:",
        
        # Диагнозы
        "tuberculosis": "🫁 Tuberculosis",
        "syphilis": "🧬 Syphilis", 
        "hiv": "🧫 HIV",
        "drug_addiction": "💊 Drug addiction",
        
        # Информация о диагнозах
        "tuberculosis_info": (
            "🫁 TUBERCULOSIS\n\n"
            "Tuberculosis is a dangerous and contagious disease that can lead to death if left untreated. It is transmitted by airborne droplets, so it's important to get examined in time. With timely diagnosis (Mantoux, Diaskin test, fluorography) tuberculosis is completely curable. Don't worry and contact the Tuberculosis Dispensary with our referral as soon as possible - GBUZ PKPTD at: Vladivostok, 4-ya Flotskaya St, 37/39. You have 10 days to visit a phthisiatrician. If necessary, the doctor may prescribe sputum culture and computed tomography of the chest organs."
        ),
        "syphilis_info": (
            "🧬 SYPHILIS\n\n"
            "Syphilis is a dangerous infectious disease transmitted primarily through sexual contact. It can be treated, especially when seeking medical attention promptly. Don't worry and contact the Dermatovenerological Dispensary with our referral as soon as possible - GBUZ KKVVD, at: Vladivostok, Gamarnika St, 18V. You have 10 days to visit a dermatovenerologist."
        ),
        "hiv_info": (
            "🧫 HIV INFECTION\n\n"
            "HIV infection is a disease caused by the human immunodeficiency virus (HIV). This virus attacks and destroys cells of the immune system that protect the body from infections.\n\n"
            "Modern antiretroviral therapy (ART) allows suppressing virus replication and significantly prolongs patients' lives. However, in Russia, treatment with these drugs is not available for legal reasons.\n\n"
            "For consultation, contact the Regional Clinical Hospital No. 2, Center for Prevention and Control of AIDS and Infectious Diseases, at: Vladivostok, Bosisenko St, 50."
        ),
        "drug_addiction_info": (
            "💊 DRUG ADDICTION\n\n"
            "Your biological material has been sent to the Regional Narcological Dispensary. Remember: a positive result may not be confirmed, so don't worry — wait for the final conclusion. If the result does turn out to be positive, it's recommended to go home and start treatment. You can also contact the Regional Narcological Dispensary at: Vladivostok, Stanyukovich St, 53, to challenge the analysis result if necessary. Wishing you all the best and good health!"
        ),
        
        # Кнопки действий
        "documents_reminder": "📋 Don't forget to bring with you:\n• passport\n• migration card\n• visa\n• registration",
        "understood_10_days": "✅ Got it",
        "understood_10_days_examination": "Got it, 10 days",
        "show_documents": "📋 Documents",
        "examination_question": "Have you completed the additional examination?",
        "passed_examination": "✅ Yes",
        "not_passed_examination": "❌ No",
        "waiting_certificate": "We are waiting for you with a certificate at LLC MO «Lotos» at the address Vladivostok, Strelkovaya 23A",
        "examination_completed": "✅ Excellent! Examination completed successfully.",
        "examination_required": "⚠️ Need to undergo examination within 10 days.",
        "not_passed_message": "❌ You did not pass the examination. Need to retake.",
        
        # Registration status
        "already_registered": "You are already registered",
        "just_registered": "You have registered",
        "user_id": "User ID",
        "registration_date": "Registration date",
        "diagnosis_date": "Diagnosis selection date",
        "deadline_date": "Deadline date",
        "status": "Status",
        "waiting_diagnosis": "Waiting for diagnosis selection",
        "choose_diagnosis": "Choose diagnosis to start examination process",
        "click_for_status": "Click button to view status:",
        "click_for_help": "Click button to view help:",
        "show_status": "📊 Show Status",
        "show_help": "❓ Show Help",
        
        # Errors
        "invalid_selection": "❌ Invalid selection. Please choose one of the provided options.",
        
        # Menu buttons
        "start_button": "🚀 Start",
        "status_button": "📊 Status",
        "help_button": "❓ Help",
        "main_menu_text": "Choose action:",
        
        # Команды бота
        "start_command": "🆔 User ID: {user_id}\n📅 Registration date: {registration_date}\n✅ {registration_status}\n⏰ Days left: {days_left}\n\n🌍 Choose language:",
        "status_command": "📊 Registration status",
        "help_command": "❓ Command help",
        
        # Описания команд для выпадающего меню
        "start_cmd_desc": "🚀 Open menu",
        "status_cmd_desc": "📊 Registration status",
        "help_cmd_desc": "❓ How does the bot work?",
        
        # Time statuses
        "days_left": "Days left: {days}",
        "last_day": "Last day!",
        "overdue": "Overdue by {days} days",
        
        # Command descriptions for dropdown menu
        "cmd_start_desc": "🚀 Open menu",
        "cmd_status_desc": "📊 Registration status",
        "cmd_help_desc": "❓ How does the bot work?",
        
        # Result
        
        # Помощь
        "help": "❓ Help",
        "help_text": "📚 BOT HELP\n\nCommands:\n/start - Start working with the bot\n/status - Find out registration status\n/help - Show this help\n\nYou have 10 days to go by referral, and within a month we will send you the commission results!",
        
        # Статус
        "no_active_case": "You have no active examinations. Press /start to start.",
        
        # Финальные уведомления
        
        
        # Сообщения об ошибках
        "error_occurred": "An error occurred. Please press /start again.",
        "choose_category": "Please choose a category from the provided buttons.",
        "examination_reminder": "✅ Thank you for your choice! Now you need to undergo an examination within 30 days from the registration date.",
        "no_active_examinations": "You have no active examinations.",
        "registration_status": "📊 REGISTRATION STATUS\n\n🆔 Your ID: {user_id}\nRegistration date: {registered_at}\nDays since registration: {days_since_registration}\n\nYou currently have no active examinations. Press /start to begin.",
        
        # Напоминания
        
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
        "action_data_show_help": "Help",
        
        # Напоминания
        "regular_reminder": "⏰ Reminder: {days_passed} have passed",
        "final_reminder": "⚠️ ATTENTION! Additional examination period has ended, your documents have been submitted to the migration service.",
        "bot_liquidation_message": "🚫 Your bot access has ended. Additional examination period has expired."
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
        return f"text not found: {key}"
    
    return TEXTS[language][key].format(**kwargs)

# Старые константы для совместимости (будут удалены)
CONSENT_TEXT = TEXTS["ru"]["consent"]
CONSENT_BUTTON_TEXT = TEXTS["ru"]["consent_button"]
CATEGORY_SELECT_TEXT = TEXTS["ru"]["category_select"]

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
FINAL_REMINDER = TEXTS["ru"]["final_reminder"]

