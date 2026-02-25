import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

BOT_TOKEN = "8372953278:AAFEHQTV0zfyynXdJreIm_pyNnBuxp6Em2w"
ADMIN_IDS = [174415647, 7321459420]

MIDDLE_USERNAME = "@CryptoDeal_Middle"
SUPPORT_USERNAME = "@CryptoDeal_Escrow"
TON_ADDRESS = "UQBu7JOWQIU72kp4r2TG45925P5Rg1qz5wzurEWmC5lWZbTL"
CARD_NUMBER = "2200702126310668"
CARD_BANK = "Озон Банк | +79011716762"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

user_data = {}
deals = {}
deal_counter = [1000]

# ===================== LANGUAGE STRINGS =====================
LANGS = {
    "ru": {
        "flag": "🇷🇺", "name": "Русский",
        "welcome": (
            "Добро пожаловать 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — специализированный сервис безопасных внебиржевых сделок.\n\n"
            "✨ Автоматизированный алгоритм исполнения.\n"
            "⚡️ Скорость и автоматизация.\n"
            "💳 Удобный и быстрый вывод средств.\n\n"
            "• Комиссия: <b>0%</b>\n"
            "• Режим работы: <b>24/7</b>\n"
            f"• Поддержка: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Создать Сделку",
        "btn_req": "🧾 Реквизиты",
        "btn_topup": "💰 Пополнить баланс",
        "btn_withdraw": "💸 Вывести средства",
        "btn_security": "🛡 Безопасность",
        "btn_support": "📋 Поддержка",
        "btn_language": "🌐 Язык",
        "btn_menu": "📱 В меню",
        "btn_cancel": "❌ Отмена",
        "btn_confirm_agreement": "📍 Подтвердить Ознакомление",
        "agreement": (
            "☑️ <b>Пользовательское соглашение</b>\n\n"
            "🛡️ Для сохранности ваших активов строго соблюдайте регламент:\n\n"
            "<b>• Депонирование активов:</b>\n"
            f"Передача только через официальный контакт: <b>{MIDDLE_USERNAME}</b>\n\n"
            "<b>• Запрет прямых расчетов:</b>\n"
            "Категорически запрещено отправлять средства напрямую.\n\n"
            "<b>• Завершение сделки:</b>\n"
            "Вывод производится автоматически после подтверждения получения.\n\n"
            "Нажмите кнопку ниже для подтверждения."
        ),
        "deal_step1": "📝 <b>Создание сделки — Шаг 1/4</b>\n\nВведите <b>@username второго участника сделки</b> (покупателя/продавца):\n\nПример: <code>@username</code>",
        "deal_step2": "📝 <b>Создание сделки — Шаг 2/4</b>\n\nВведите <b>суть сделки</b> (что продаёте/покупаете):",
        "deal_step3": "📝 <b>Создание сделки — Шаг 3/4</b>\n\nВведите <b>сумму сделки</b>:",
        "deal_step4": "📝 <b>Создание сделки — Шаг 4/4</b>\n\nВ чём хотите получить оплату?",
        "deal_created": (
            "✅ <b>Сделка успешно создана!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 Второй участник: <b>{partner}</b>\n"
            "📋 Суть: {description}\n"
            "💵 Сумма: {amount}\n"
            "💱 Валюта: {currency}\n"
            "🔗 Ссылка для участника: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>ВАЖНО — КАК ПРОХОДИТ СДЕЛКА:</b>\n\n"
            f"1️⃣ Продавец передаёт актив менеджеру: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер проверяет получение в течение <b>5 минут</b>\n"
            f"3️⃣ После подтверждения покупатель отправляет оплату\n"
            f"4️⃣ Менеджер верифицирует оплату и передаёт актив покупателю\n\n"
            f"⚠️ Никогда не передавайте активы напрямую — только через {MIDDLE_USERNAME}\n"
            "⏱ Среднее время сделки: <b>5–15 минут</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Статус: <b>Активна</b>"
        ),
        "deal_info": (
            "📋 <b>Информация о сделке</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Суть: {description}\n"
            "💵 Сумма: {amount}\n"
            "💱 Валюта: {currency}\n"
            "🔘 Статус: <b>Активна</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>КАК ПРОХОДИТ СДЕЛКА:</b>\n\n"
            f"1️⃣ Продавец передаёт актив менеджеру: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер подтверждает получение в течение <b>5 минут</b>\n"
            f"3️⃣ Покупатель отправляет оплату\n"
            f"4️⃣ Менеджер верифицирует и закрывает сделку\n\n"
            f"⚠️ Передавайте активы только через {MIDDLE_USERNAME}\n"
            "⏱ Среднее время: <b>5–15 минут</b>\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "btn_write_middle": "💬 Написать менеджеру",
        "own_deal": "⚠️ Это ваша собственная сделка.",
        "deal_not_found": "❌ Сделка не найдена или уже завершена.",
        "partner_notified": "👤 По вашей сделке <code>{deal_id}</code> перешёл: <b>{buyer}</b>",
        "req_title": "🧾 <b>Реквизиты</b>\n\n💎 TON: <code>{ton}</code>\n💳 Карта: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 Реквизит для <b>{cur}</b> не добавлен. Добавьте и создайте сделку заново.",
        "ton_saved": "✅ TON кошелёк сохранён!",
        "card_saved": "✅ Карта сохранена!",
        "stars_saved": "✅ Username для Stars сохранён!",
        "redo_deal": "\n\nТеперь создайте сделку заново.",
        "enter_ton": "💎 Введите ваш <b>TON кошелёк</b>:",
        "enter_card": "💳 Введите <b>номер карты</b>:",
        "enter_stars": "⭐️ Введите ваш <b>Telegram username</b> для Stars:",
        "topup_title": "💰 <b>Пополнение баланса</b>\n\nВыберите способ:",
        "withdraw_text": f"💸 <b>Вывод средств</b>\n\nОбратитесь в поддержку:\n👤 {MIDDLE_USERNAME}\n\n⚠️ Укажите сумму и реквизиты.",
        "security": (
            "🛡 <b>БЕЗОПАСНОСТЬ ПРИ ПЕРЕДАЧЕ АКТИВОВ</b>\n\n"
            f"Передача производится исключительно через: <b>{MIDDLE_USERNAME}</b>\n\n"
            "<b>• Запрет прямых транзакций:</b> активы напрямую не передаются.\n"
            "<b>• Верификация:</b> сверяйте сумму и тег сделки.\n"
            "<b>• Завершение:</b> вывод после подтверждения обеими сторонами."
        ),
        "lang_choose": "🌐 <b>Выберите язык:</b>",
        "lang_set": "✅ Язык установлен: Русский 🇷🇺",
        "topup_stars": (
            f"⭐️ <b>Пополнение Stars</b>\n\nПередайте Stars на: <b>{MIDDLE_USERNAME}</b>\n\n"
            "• Перейдите в диалог и отправьте Stars.\n"
            "• Баланс пополнится автоматически.\n\n⏱ Зачисление: <b>5–15 минут</b>"
        ),
        "topup_ton": (
            f"💎 <b>Пополнение TON</b>\n\n<code>{TON_ADDRESS}</code>\n\n"
            f"После отправки напишите в поддержку: <b>{MIDDLE_USERNAME}</b>\n\n⏱ Зачисление: <b>5–15 минут</b>"
        ),
        "topup_card": (
            f"💳 <b>Пополнение картой</b>\n\nРеквизиты:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n"
            "• Сохраните чек.\n• Обратитесь в поддержку.\n\n⏱ Зачисление: <b>5–15 минут</b>"
        ),
        "topup_nft": (
            f"🎁 <b>Пополнение NFT</b>\n\nПередайте актив: <b>{MIDDLE_USERNAME}</b>\n\n"
            "• После верификации оценка в Stars или TON.\n\n⏱ Зачисление: <b>5–15 минут</b>"
        ),
        "invalid_username": "❌ Введите корректный @username (начинается с @):",
    },
    "en": {
        "flag": "🇬🇧", "name": "English",
        "welcome": (
            "Welcome 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — secure OTC deal service.\n\n"
            "✨ Automated execution algorithm.\n"
            "⚡️ Speed and automation.\n"
            "💳 Fast and convenient withdrawal.\n\n"
            "• Commission: <b>0%</b>\n"
            "• Working hours: <b>24/7</b>\n"
            f"• Support: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Create Deal",
        "btn_req": "🧾 Requisites",
        "btn_topup": "💰 Top Up Balance",
        "btn_withdraw": "💸 Withdraw",
        "btn_security": "🛡 Security",
        "btn_support": "📋 Support",
        "btn_language": "🌐 Language",
        "btn_menu": "📱 Menu",
        "btn_cancel": "❌ Cancel",
        "btn_confirm_agreement": "📍 Confirm Agreement",
        "agreement": (
            "☑️ <b>User Agreement</b>\n\n"
            "🛡️ To protect your assets, follow the rules:\n\n"
            "<b>• Asset deposit:</b>\n"
            f"Transfer only through: <b>{MIDDLE_USERNAME}</b>\n\n"
            "<b>• No direct payments:</b>\n"
            "Sending funds directly is strictly prohibited.\n\n"
            "<b>• Deal completion:</b>\n"
            "Withdrawal is processed automatically after confirmation.\n\n"
            "Press the button below to confirm."
        ),
        "deal_step1": "📝 <b>Create Deal — Step 1/4</b>\n\nEnter the <b>@username of the second participant</b> (buyer/seller):\n\nExample: <code>@username</code>",
        "deal_step2": "📝 <b>Create Deal — Step 2/4</b>\n\nDescribe the <b>deal</b> (what you're buying/selling):",
        "deal_step3": "📝 <b>Create Deal — Step 3/4</b>\n\nEnter the <b>deal amount</b>:",
        "deal_step4": "📝 <b>Create Deal — Step 4/4</b>\n\nWhat currency do you want to receive?",
        "deal_created": (
            "✅ <b>Deal successfully created!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 Second participant: <b>{partner}</b>\n"
            "📋 Description: {description}\n"
            "💵 Amount: {amount}\n"
            "💱 Currency: {currency}\n"
            "🔗 Link for participant: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>HOW THE DEAL WORKS:</b>\n\n"
            f"1️⃣ Seller transfers asset to manager: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Manager confirms receipt within <b>5 minutes</b>\n"
            f"3️⃣ Buyer sends payment\n"
            f"4️⃣ Manager verifies and releases the asset\n\n"
            f"⚠️ Never transfer assets directly — only through {MIDDLE_USERNAME}\n"
            "⏱ Average deal time: <b>5–15 minutes</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Status: <b>Active</b>"
        ),
        "deal_info": (
            "📋 <b>Deal Information</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Description: {description}\n"
            "💵 Amount: {amount}\n"
            "💱 Currency: {currency}\n"
            "🔘 Status: <b>Active</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 <b>HOW THE DEAL WORKS:</b>\n\n"
            f"1️⃣ Seller transfers asset to manager: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Manager confirms within <b>5 minutes</b>\n"
            f"3️⃣ Buyer sends payment\n"
            f"4️⃣ Manager verifies and closes the deal\n\n"
            f"⚠️ Transfer assets only through {MIDDLE_USERNAME}\n"
            "⏱ Average time: <b>5–15 minutes</b>\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "btn_write_middle": "💬 Write to Manager",
        "own_deal": "⚠️ This is your own deal.",
        "deal_not_found": "❌ Deal not found or already closed.",
        "partner_notified": "👤 User <b>{buyer}</b> joined your deal <code>{deal_id}</code>",
        "req_title": "🧾 <b>Requisites</b>\n\n💎 TON: <code>{ton}</code>\n💳 Card: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 Requisite for <b>{cur}</b> not added. Add it and create the deal again.",
        "ton_saved": "✅ TON wallet saved!",
        "card_saved": "✅ Card saved!",
        "stars_saved": "✅ Stars username saved!",
        "redo_deal": "\n\nNow create the deal again.",
        "enter_ton": "💎 Enter your <b>TON wallet</b>:",
        "enter_card": "💳 Enter your <b>card number</b>:",
        "enter_stars": "⭐️ Enter your <b>Telegram username</b> for Stars:",
        "topup_title": "💰 <b>Top Up Balance</b>\n\nChoose method:",
        "withdraw_text": f"💸 <b>Withdrawal</b>\n\nContact support:\n👤 {MIDDLE_USERNAME}\n\n⚠️ Specify amount and requisites.",
        "security": (
            "🛡 <b>ASSET TRANSFER SECURITY</b>\n\n"
            f"Transfer exclusively through: <b>{MIDDLE_USERNAME}</b>\n\n"
            "<b>• No direct transactions:</b> assets are never sent directly.\n"
            "<b>• Verification:</b> check the amount and deal tag.\n"
            "<b>• Completion:</b> withdrawal after both sides confirm."
        ),
        "lang_choose": "🌐 <b>Choose language:</b>",
        "lang_set": "✅ Language set: English 🇬🇧",
        "topup_stars": (
            f"⭐️ <b>Top Up with Stars</b>\n\nSend Stars to: <b>{MIDDLE_USERNAME}</b>\n\n"
            "• Open the dialog and send Stars.\n"
            "• Balance will be credited automatically.\n\n⏱ Processing: <b>5–15 minutes</b>"
        ),
        "topup_ton": (
            f"💎 <b>Top Up with TON</b>\n\n<code>{TON_ADDRESS}</code>\n\n"
            f"After sending, contact support: <b>{MIDDLE_USERNAME}</b>\n\n⏱ Processing: <b>5–15 minutes</b>"
        ),
        "topup_card": (
            f"💳 <b>Top Up with Card</b>\n\nDetails:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n"
            "• Save your receipt.\n• Contact support.\n\n⏱ Processing: <b>5–15 minutes</b>"
        ),
        "topup_nft": (
            f"🎁 <b>Top Up with NFT</b>\n\nTransfer asset to: <b>{MIDDLE_USERNAME}</b>\n\n"
            "• After verification, valued in Stars or TON.\n\n⏱ Processing: <b>5–15 minutes</b>"
        ),
        "invalid_username": "❌ Enter a valid @username (must start with @):",
    },
    "az": {
        "flag": "🇦🇿", "name": "Azərbaycanca",
        "welcome": (
            "Xoş gəldiniz 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — təhlükəsiz OTC sövdələşmə xidməti.\n\n"
            "✨ Avtomatlaşdırılmış icra.\n"
            "⚡️ Sürət və avtomatlaşdırma.\n"
            "💳 Rahat çıxarış.\n\n"
            "• Komissiya: <b>0%</b>\n"
            "• İş rejimi: <b>24/7</b>\n"
            f"• Dəstək: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Sövdələşmə Yarat",
        "btn_req": "🧾 Rekvizitlər",
        "btn_topup": "💰 Balansı Artır",
        "btn_withdraw": "💸 Çıxarış",
        "btn_security": "🛡 Təhlükəsizlik",
        "btn_support": "📋 Dəstək",
        "btn_language": "🌐 Dil",
        "btn_menu": "📱 Menyu",
        "btn_cancel": "❌ Ləğv et",
        "btn_confirm_agreement": "📍 Razılığı Təsdiqləyin",
        "agreement": (
            "☑️ <b>İstifadəçi Razılaşması</b>\n\n"
            f"Aktivlər yalnız: <b>{MIDDLE_USERNAME}</b> vasitəsilə ötürülür.\n\n"
            "Birbaşa ödəniş qadağandır.\n\n"
            "Aşağıdakı düyməni basın."
        ),
        "deal_step1": "📝 <b>Sövdələşmə — Addım 1/4</b>\n\nİkinci iştirakçının <b>@username</b>-ni daxil edin:",
        "deal_step2": "📝 <b>Sövdələşmə — Addım 2/4</b>\n\n<b>Sövdələşmənin mahiyyətini</b> daxil edin:",
        "deal_step3": "📝 <b>Sövdələşmə — Addım 3/4</b>\n\n<b>Məbləği</b> daxil edin:",
        "deal_step4": "📝 <b>Sövdələşmə — Addım 4/4</b>\n\nHansı valyutada almaq istərsiniz?",
        "deal_created": (
            "✅ <b>Sövdələşmə yaradıldı!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 İkinci iştirakçı: <b>{partner}</b>\n"
            "📋 Məzmun: {description}\n"
            "💵 Məbləğ: {amount}\n"
            "💱 Valyuta: {currency}\n"
            "🔗 Link: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Satıcı aktivi menecerə göndərir: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Menecer <b>5 dəqiqə</b> ərzində təsdiqləyir\n"
            f"3️⃣ Alıcı ödəniş göndərir\n"
            f"4️⃣ Menecer doğrulayır və aktivi ötürür\n\n"
            f"⚠️ Aktivləri yalnız {MIDDLE_USERNAME} vasitəsilə ötürün\n"
            "⏱ Orta müddət: <b>5–15 dəqiqə</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Status: <b>Aktiv</b>"
        ),
        "deal_info": (
            "📋 <b>Sövdələşmə Məlumatı</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Məzmun: {description}\n"
            "💵 Məbləğ: {amount}\n"
            "💱 Valyuta: {currency}\n\n"
            f"1️⃣ Satıcı aktivi menecerə göndərir: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Menecer <b>5 dəqiqə</b> ərzində təsdiqləyir\n"
            f"⚠️ Yalnız {MIDDLE_USERNAME} vasitəsilə\n"
            "⏱ Orta müddət: <b>5–15 dəqiqə</b>"
        ),
        "btn_write_middle": "💬 Menecerə Yaz",
        "own_deal": "⚠️ Bu sizin öz sövdələşmənizdır.",
        "deal_not_found": "❌ Sövdələşmə tapılmadı.",
        "partner_notified": "👤 İstifadəçi <b>{buyer}</b> sövdələşməyə qoşuldu <code>{deal_id}</code>",
        "req_title": "🧾 <b>Rekvizitlər</b>\n\n💎 TON: <code>{ton}</code>\n💳 Kart: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 <b>{cur}</b> üçün rekvizit əlavə edilməyib.",
        "ton_saved": "✅ TON cüzdanı saxlanıldı!",
        "card_saved": "✅ Kart saxlanıldı!",
        "stars_saved": "✅ Stars username saxlanıldı!",
        "redo_deal": "\n\nİndi sövdələşməni yenidən yaradın.",
        "enter_ton": "💎 <b>TON cüzdanınızı</b> daxil edin:",
        "enter_card": "💳 <b>Kart nömrəsini</b> daxil edin:",
        "enter_stars": "⭐️ Stars üçün <b>Telegram username</b>-nizi daxil edin:",
        "topup_title": "💰 <b>Balansı Artır</b>\n\nÜsul seçin:",
        "withdraw_text": f"💸 <b>Çıxarış</b>\n\nDəstəklə əlaqə saxlayın:\n👤 {MIDDLE_USERNAME}",
        "security": f"🛡 <b>Təhlükəsizlik</b>\n\nAktivlər yalnız {MIDDLE_USERNAME} vasitəsilə ötürülür.",
        "lang_choose": "🌐 <b>Dil seçin:</b>",
        "lang_set": "✅ Dil təyin edildi: Azərbaycanca 🇦🇿",
        "topup_stars": f"⭐️ Stars göndərin: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 dəqiqə</b>",
        "topup_ton": f"💎 TON ünvanı:\n<code>{TON_ADDRESS}</code>\n\n{MIDDLE_USERNAME}\n\n⏱ <b>5–15 dəqiqə</b>",
        "topup_card": f"💳 Kart:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n⏱ <b>5–15 dəqiqə</b>",
        "topup_nft": f"🎁 NFT göndərin: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 dəqiqə</b>",
        "invalid_username": "❌ Düzgün @username daxil edin:",
    },
    "tr": {
        "flag": "🇹🇷", "name": "Türkçe",
        "welcome": (
            "Hoş geldiniz 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — güvenli OTC işlem hizmeti.\n\n"
            "✨ Otomatik yürütme.\n"
            "⚡️ Hız ve otomasyon.\n"
            "💳 Hızlı çekim.\n\n"
            "• Komisyon: <b>0%</b>\n"
            "• Çalışma saatleri: <b>24/7</b>\n"
            f"• Destek: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Anlaşma Oluştur",
        "btn_req": "🧾 Ödeme Bilgileri",
        "btn_topup": "💰 Bakiye Yükle",
        "btn_withdraw": "💸 Para Çek",
        "btn_security": "🛡 Güvenlik",
        "btn_support": "📋 Destek",
        "btn_language": "🌐 Dil",
        "btn_menu": "📱 Menü",
        "btn_cancel": "❌ İptal",
        "btn_confirm_agreement": "📍 Sözleşmeyi Onayla",
        "agreement": (
            "☑️ <b>Kullanıcı Sözleşmesi</b>\n\n"
            f"Varlıklar yalnızca: <b>{MIDDLE_USERNAME}</b> üzerinden transfer edilir.\n\n"
            "Doğrudan ödeme yasaktır.\n\n"
            "Onaylamak için butona basın."
        ),
        "deal_step1": "📝 <b>Anlaşma — Adım 1/4</b>\n\nİkinci katılımcının <b>@username</b>'ini girin:",
        "deal_step2": "📝 <b>Anlaşma — Adım 2/4</b>\n\n<b>Anlaşmanın konusunu</b> girin:",
        "deal_step3": "📝 <b>Anlaşma — Adım 3/4</b>\n\n<b>Tutarı</b> girin:",
        "deal_step4": "📝 <b>Anlaşma — Adım 4/4</b>\n\nHangi para biriminde almak istiyorsunuz?",
        "deal_created": (
            "✅ <b>Anlaşma oluşturuldu!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 İkinci katılımcı: <b>{partner}</b>\n"
            "📋 Konu: {description}\n"
            "💵 Tutar: {amount}\n"
            "💱 Para birimi: {currency}\n"
            "🔗 Link: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Satıcı varlığı yöneticiye gönderir: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Yönetici <b>5 dakika</b> içinde onaylar\n"
            f"3️⃣ Alıcı ödeme gönderir\n"
            f"4️⃣ Yönetici doğrular ve varlığı teslim eder\n\n"
            f"⚠️ Varlıkları yalnızca {MIDDLE_USERNAME} üzerinden gönderin\n"
            "⏱ Ortalama süre: <b>5–15 dakika</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Durum: <b>Aktif</b>"
        ),
        "deal_info": (
            "📋 <b>Anlaşma Bilgisi</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Konu: {description}\n"
            "💵 Tutar: {amount}\n"
            "💱 Para birimi: {currency}\n\n"
            f"1️⃣ Satıcı varlığı yöneticiye gönderir: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Yönetici <b>5 dakika</b> içinde onaylar\n"
            f"⚠️ Yalnızca {MIDDLE_USERNAME} üzerinden\n"
            "⏱ Ortalama: <b>5–15 dakika</b>"
        ),
        "btn_write_middle": "💬 Yöneticiye Yaz",
        "own_deal": "⚠️ Bu sizin kendi anlaşmanız.",
        "deal_not_found": "❌ Anlaşma bulunamadı.",
        "partner_notified": "👤 Kullanıcı <b>{buyer}</b> anlaşmaya katıldı <code>{deal_id}</code>",
        "req_title": "🧾 <b>Ödeme Bilgileri</b>\n\n💎 TON: <code>{ton}</code>\n💳 Kart: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 <b>{cur}</b> için ödeme bilgisi eklenmedi.",
        "ton_saved": "✅ TON cüzdanı kaydedildi!",
        "card_saved": "✅ Kart kaydedildi!",
        "stars_saved": "✅ Stars kullanıcı adı kaydedildi!",
        "redo_deal": "\n\nŞimdi anlaşmayı yeniden oluşturun.",
        "enter_ton": "💎 <b>TON cüzdanınızı</b> girin:",
        "enter_card": "💳 <b>Kart numaranızı</b> girin:",
        "enter_stars": "⭐️ Stars için <b>Telegram kullanıcı adını</b> girin:",
        "topup_title": "💰 <b>Bakiye Yükle</b>\n\nYöntem seçin:",
        "withdraw_text": f"💸 <b>Para Çekme</b>\n\nDestekle iletişime geçin:\n👤 {MIDDLE_USERNAME}",
        "security": f"🛡 <b>Güvenlik</b>\n\nVarlıklar yalnızca {MIDDLE_USERNAME} üzerinden transfer edilir.",
        "lang_choose": "🌐 <b>Dil seçin:</b>",
        "lang_set": "✅ Dil ayarlandı: Türkçe 🇹🇷",
        "topup_stars": f"⭐️ Stars gönderin: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 dakika</b>",
        "topup_ton": f"💎 TON adresi:\n<code>{TON_ADDRESS}</code>\n\n{MIDDLE_USERNAME}\n\n⏱ <b>5–15 dakika</b>",
        "topup_card": f"💳 Kart:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n⏱ <b>5–15 dakika</b>",
        "topup_nft": f"🎁 NFT gönderin: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 dakika</b>",
        "invalid_username": "❌ Geçerli bir @username girin:",
    },
    "kz": {
        "flag": "🇰🇿", "name": "Қазақша",
        "welcome": (
            "Қош келдіңіз 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — қауіпсіз OTC мәмілелер қызметі.\n\n"
            "✨ Автоматтандырылған орындау.\n"
            "⚡️ Жылдамдық және автоматтандыру.\n"
            "💳 Ыңғайлы шығару.\n\n"
            "• Комиссия: <b>0%</b>\n"
            "• Жұмыс уақыты: <b>24/7</b>\n"
            f"• Қолдау: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Мәміле Жасау",
        "btn_req": "🧾 Реквизиттер",
        "btn_topup": "💰 Балансты Толтыру",
        "btn_withdraw": "💸 Шығару",
        "btn_security": "🛡 Қауіпсіздік",
        "btn_support": "📋 Қолдау",
        "btn_language": "🌐 Тіл",
        "btn_menu": "📱 Мәзір",
        "btn_cancel": "❌ Болдырмау",
        "btn_confirm_agreement": "📍 Келісімді Растау",
        "agreement": (
            "☑️ <b>Пайдаланушы келісімі</b>\n\n"
            f"Активтер тек: <b>{MIDDLE_USERNAME}</b> арқылы беріледі.\n\n"
            "Тікелей төлем қадаған.\n\n"
            "Растау үшін батырманы басыңыз."
        ),
        "deal_step1": "📝 <b>Мәміле — Қадам 1/4</b>\n\nЕкінші қатысушының <b>@username</b>-ін енгізіңіз:",
        "deal_step2": "📝 <b>Мәміле — Қадам 2/4</b>\n\n<b>Мәміленің мәнін</b> енгізіңіз:",
        "deal_step3": "📝 <b>Мәміле — Қадам 3/4</b>\n\n<b>Сомасын</b> енгізіңіз:",
        "deal_step4": "📝 <b>Мәміле — Қадам 4/4</b>\n\nҚандай валютада алғыңыз келеді?",
        "deal_created": (
            "✅ <b>Мәміле жасалды!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 Екінші қатысушы: <b>{partner}</b>\n"
            "📋 Мән: {description}\n"
            "💵 Сома: {amount}\n"
            "💱 Валюта: {currency}\n"
            "🔗 Сілтеме: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Сатушы активті менеджерге жібереді: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер <b>5 минут</b> ішінде растайды\n"
            f"3️⃣ Сатып алушы төлем жібереді\n"
            f"4️⃣ Менеджер тексеріп активті береді\n\n"
            f"⚠️ Активтерді тек {MIDDLE_USERNAME} арқылы жіберіңіз\n"
            "⏱ Орташа уақыт: <b>5–15 минут</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Күй: <b>Белсенді</b>"
        ),
        "deal_info": (
            "📋 <b>Мәміле туралы ақпарат</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Мән: {description}\n"
            "💵 Сома: {amount}\n"
            "💱 Валюта: {currency}\n\n"
            f"1️⃣ Сатушы активті менеджерге жібереді: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер <b>5 минут</b> ішінде растайды\n"
            f"⚠️ Тек {MIDDLE_USERNAME} арқылы\n"
            "⏱ Орташа: <b>5–15 минут</b>"
        ),
        "btn_write_middle": "💬 Менеджерге Жаз",
        "own_deal": "⚠️ Бұл сіздің өз мәмілеңіз.",
        "deal_not_found": "❌ Мәміле табылмады.",
        "partner_notified": "👤 Пайдаланушы <b>{buyer}</b> мәмілеге қосылды <code>{deal_id}</code>",
        "req_title": "🧾 <b>Реквизиттер</b>\n\n💎 TON: <code>{ton}</code>\n💳 Карта: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 <b>{cur}</b> үшін реквизит қосылмаған.",
        "ton_saved": "✅ TON әмиян сақталды!",
        "card_saved": "✅ Карта сақталды!",
        "stars_saved": "✅ Stars username сақталды!",
        "redo_deal": "\n\nЕнді мәмілені қайта жасаңыз.",
        "enter_ton": "💎 <b>TON әмияныңызды</b> енгізіңіз:",
        "enter_card": "💳 <b>Карта нөмірін</b> енгізіңіз:",
        "enter_stars": "⭐️ Stars үшін <b>Telegram username</b>-іңізді енгізіңіз:",
        "topup_title": "💰 <b>Балансты Толтыру</b>\n\nТәсілді таңдаңыз:",
        "withdraw_text": f"💸 <b>Шығару</b>\n\nҚолдаумен байланысыңыз:\n👤 {MIDDLE_USERNAME}",
        "security": f"🛡 <b>Қауіпсіздік</b>\n\nАктивтер тек {MIDDLE_USERNAME} арқылы беріледі.",
        "lang_choose": "🌐 <b>Тілді таңдаңыз:</b>",
        "lang_set": "✅ Тіл орнатылды: Қазақша 🇰🇿",
        "topup_stars": f"⭐️ Stars жіберіңіз: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 минут</b>",
        "topup_ton": f"💎 TON мекенжайы:\n<code>{TON_ADDRESS}</code>\n\n{MIDDLE_USERNAME}\n\n⏱ <b>5–15 минут</b>",
        "topup_card": f"💳 Карта:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n⏱ <b>5–15 минут</b>",
        "topup_nft": f"🎁 NFT жіберіңіз: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 минут</b>",
        "invalid_username": "❌ Дұрыс @username енгізіңіз:",
    },
    "ua": {
        "flag": "🇺🇦", "name": "Українська",
        "welcome": (
            "Ласкаво просимо 👋\n\n"
            "💼 <b>Crypto Deals • Middle</b> — безпечний OTC сервіс угод.\n\n"
            "✨ Автоматизоване виконання.\n"
            "⚡️ Швидкість та автоматизація.\n"
            "💳 Зручне виведення.\n\n"
            "• Комісія: <b>0%</b>\n"
            "• Режим роботи: <b>24/7</b>\n"
            f"• Підтримка: <b>{MIDDLE_USERNAME}</b>"
        ),
        "btn_deal": "🔐 Створити Угоду",
        "btn_req": "🧾 Реквізити",
        "btn_topup": "💰 Поповнити Баланс",
        "btn_withdraw": "💸 Вивести Кошти",
        "btn_security": "🛡 Безпека",
        "btn_support": "📋 Підтримка",
        "btn_language": "🌐 Мова",
        "btn_menu": "📱 Меню",
        "btn_cancel": "❌ Скасувати",
        "btn_confirm_agreement": "📍 Підтвердити Ознайомлення",
        "agreement": (
            "☑️ <b>Угода користувача</b>\n\n"
            f"Активи передаються лише через: <b>{MIDDLE_USERNAME}</b>\n\n"
            "Прямі платежі заборонені.\n\n"
            "Натисніть кнопку нижче."
        ),
        "deal_step1": "📝 <b>Угода — Крок 1/4</b>\n\nВведіть <b>@username другого учасника</b>:",
        "deal_step2": "📝 <b>Угода — Крок 2/4</b>\n\nВведіть <b>суть угоди</b>:",
        "deal_step3": "📝 <b>Угода — Крок 3/4</b>\n\nВведіть <b>суму угоди</b>:",
        "deal_step4": "📝 <b>Угода — Крок 4/4</b>\n\nУ якій валюті бажаєте отримати?",
        "deal_created": (
            "✅ <b>Угоду створено!</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "👤 Другий учасник: <b>{partner}</b>\n"
            "📋 Суть: {description}\n"
            "💵 Сума: {amount}\n"
            "💱 Валюта: {currency}\n"
            "🔗 Посилання: <code>https://t.me/{bot_username}?start=deal_{deal_id}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Продавець передає актив менеджеру: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер підтверджує протягом <b>5 хвилин</b>\n"
            f"3️⃣ Покупець надсилає оплату\n"
            f"4️⃣ Менеджер верифікує та передає актив\n\n"
            f"⚠️ Передавайте активи лише через {MIDDLE_USERNAME}\n"
            "⏱ Середній час: <b>5–15 хвилин</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏳ Статус: <b>Активна</b>"
        ),
        "deal_info": (
            "📋 <b>Інформація про угоду</b>\n\n"
            "🆔 ID: <code>{deal_id}</code>\n"
            "📝 Суть: {description}\n"
            "💵 Сума: {amount}\n"
            "💱 Валюта: {currency}\n\n"
            f"1️⃣ Продавець передає актив менеджеру: <b>{MIDDLE_USERNAME}</b>\n"
            f"2️⃣ Менеджер підтверджує протягом <b>5 хвилин</b>\n"
            f"⚠️ Лише через {MIDDLE_USERNAME}\n"
            "⏱ Середній час: <b>5–15 хвилин</b>"
        ),
        "btn_write_middle": "💬 Написати менеджеру",
        "own_deal": "⚠️ Це ваша власна угода.",
        "deal_not_found": "❌ Угоду не знайдено.",
        "partner_notified": "👤 Користувач <b>{buyer}</b> приєднався до угоди <code>{deal_id}</code>",
        "req_title": "🧾 <b>Реквізити</b>\n\n💎 TON: <code>{ton}</code>\n💳 Картка: <code>{card}</code>\n⭐️ Stars: <code>{stars}</code>",
        "no_req": "📎 Реквізит для <b>{cur}</b> не додано.",
        "ton_saved": "✅ TON гаманець збережено!",
        "card_saved": "✅ Картку збережено!",
        "stars_saved": "✅ Username для Stars збережено!",
        "redo_deal": "\n\nТепер створіть угоду знову.",
        "enter_ton": "💎 Введіть ваш <b>TON гаманець</b>:",
        "enter_card": "💳 Введіть <b>номер картки</b>:",
        "enter_stars": "⭐️ Введіть ваш <b>Telegram username</b> для Stars:",
        "topup_title": "💰 <b>Поповнення балансу</b>\n\nОберіть спосіб:",
        "withdraw_text": f"💸 <b>Виведення коштів</b>\n\nЗверніться до підтримки:\n👤 {MIDDLE_USERNAME}",
        "security": f"🛡 <b>Безпека</b>\n\nАктиви передаються лише через {MIDDLE_USERNAME}.",
        "lang_choose": "🌐 <b>Оберіть мову:</b>",
        "lang_set": "✅ Мова встановлена: Українська 🇺🇦",
        "topup_stars": f"⭐️ Надішліть Stars: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 хвилин</b>",
        "topup_ton": f"💎 TON адреса:\n<code>{TON_ADDRESS}</code>\n\n{MIDDLE_USERNAME}\n\n⏱ <b>5–15 хвилин</b>",
        "topup_card": f"💳 Картка:\n<code>{CARD_NUMBER}</code>\n{CARD_BANK}\n\n⏱ <b>5–15 хвилин</b>",
        "topup_nft": f"🎁 Передайте NFT: <b>{MIDDLE_USERNAME}</b>\n\n⏱ <b>5–15 хвилин</b>",
        "invalid_username": "❌ Введіть коректний @username:",
    },
}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"ton_wallet": "", "card": "", "username_stars": "", "has_requisites": False,
                          "balance": 0.0, "reputation": 0, "deals_count": 0, "reviews": [], "lang": "ru"}
    return user_data[uid]

def get_lang(uid):
    return get_user(uid).get("lang", "ru")

def L(uid, key, **kwargs):
    lang = get_lang(uid)
    text = LANGS.get(lang, LANGS["ru"]).get(key, LANGS["ru"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text

def gen_deal_id():
    deal_counter[0] += 1
    return f"CD{deal_counter[0]}"

username_map = {}

def find_uid(query: str):
    q = query.strip()
    if q.startswith("@"):
        return username_map.get(q[1:].lower())
    try:
        uid = int(q)
        return uid if uid in user_data else None
    except ValueError:
        return None

# ===================== STATES =====================
class SetBanner(StatesGroup):
    waiting = State()

class AddReq(StatesGroup):
    ton = State()
    card = State()
    stars = State()

class Deal(StatesGroup):
    partner = State()
    description = State()
    amount = State()
    currency = State()

class AdminAction(StatesGroup):
    reputation = State()
    balance = State()
    review = State()

# ===================== KEYBOARDS =====================
def main_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L(uid,"btn_deal"), callback_data="deal"),
         InlineKeyboardButton(text=L(uid,"btn_req"), callback_data="requisites")],
        [InlineKeyboardButton(text=L(uid,"btn_topup"), callback_data="topup"),
         InlineKeyboardButton(text=L(uid,"btn_withdraw"), callback_data="withdraw")],
        [InlineKeyboardButton(text=L(uid,"btn_security"), callback_data="security"),
         InlineKeyboardButton(text=L(uid,"btn_support"), url="https://t.me/CryptoDeal_Middle")],
        [InlineKeyboardButton(text=L(uid,"btn_language"), callback_data="language")],
    ])

def back_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=L(uid,"btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def cancel_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L(uid,"btn_cancel"), callback_data="menu")]
    ])

def agreement_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=L(uid,"btn_confirm_agreement"), callback_data="confirm_agreement")],
        [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=L(uid,"btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def currency_kb(uid):
    lang = get_lang(uid)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="deal_cur_ton"),
         InlineKeyboardButton(text="⭐️ Stars", callback_data="deal_cur_stars")],
        [InlineKeyboardButton(text="💳 " + ("Карта (RUB)" if lang == "ru" else "Card (RUB)" if lang == "en" else "Kart (RUB)" if lang in ("tr","az") else "Картка (RUB)" if lang == "ua" else "Карта (RUB)"), callback_data="deal_cur_card"),
         InlineKeyboardButton(text="🎁 NFT", callback_data="deal_cur_nft")],
        [InlineKeyboardButton(text=L(uid,"btn_cancel"), callback_data="menu")],
    ])

def req_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="req_ton"),
         InlineKeyboardButton(text="💳 " + ("Карта" if get_lang(uid) in ("ru","kz") else "Card" if get_lang(uid) == "en" else "Kart" if get_lang(uid) in ("tr","az") else "Картка"), callback_data="req_card")],
        [InlineKeyboardButton(text="⭐️ Username Stars", callback_data="req_stars")],
        [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")],
    ])

def add_req_kb(uid, req_type):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ " + ("Добавить" if get_lang(uid) == "ru" else "Add" if get_lang(uid) == "en" else "Əlavə et" if get_lang(uid) == "az" else "Ekle" if get_lang(uid) == "tr" else "Қосу" if get_lang(uid) == "kz" else "Додати"), callback_data=f"req_{req_type}_deal")],
        [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")],
    ])

def topup_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐️ Stars", callback_data="topup_stars"),
         InlineKeyboardButton(text="💎 TON", callback_data="topup_ton")],
        [InlineKeyboardButton(text="💳 " + ("Карта" if get_lang(uid) in ("ru","kz","ua") else "Card" if get_lang(uid) == "en" else "Kart"), callback_data="topup_card"),
         InlineKeyboardButton(text="🎁 NFT", callback_data="topup_nft")],
        [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=L(uid,"btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def language_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang_ru"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="setlang_en")],
        [InlineKeyboardButton(text="🇦🇿 Azərbaycanca", callback_data="setlang_az"),
         InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="setlang_tr")],
        [InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="setlang_kz"),
         InlineKeyboardButton(text="🇺🇦 Українська", callback_data="setlang_ua")],
    ])

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Баннер", callback_data="adm_banner"),
         InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="adm_users"),
         InlineKeyboardButton(text="⭐️ Репутация", callback_data="adm_reputation")],
        [InlineKeyboardButton(text="💬 Отзыв", callback_data="adm_review"),
         InlineKeyboardButton(text="💰 Баланс", callback_data="adm_balance")],
        [InlineKeyboardButton(text="📋 Сделки", callback_data="adm_deals")],
    ])

# ===================== HELPERS =====================
async def safe_delete(msg):
    try:
        await msg.delete()
    except Exception:
        pass

async def show_menu(message: Message, uid: int):
    banner = user_data.get("_banner")
    welcome = L(uid, "welcome")
    kb = main_kb(uid)
    if banner:
        await message.answer_photo(photo=banner["photo_id"],
                                   caption=banner.get("caption") or welcome,
                                   parse_mode="HTML", reply_markup=kb)
    else:
        await message.answer(welcome, parse_mode="HTML", reply_markup=kb)

def _reg(msg: Message):
    if msg.from_user and msg.from_user.username:
        username_map[msg.from_user.username.lower()] = msg.from_user.id

# ===================== /START =====================
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    uid = message.from_user.id
    get_user(uid)
    if message.from_user.username:
        username_map[message.from_user.username.lower()] = uid
    await safe_delete(message)

    args = message.text.split()
    if len(args) > 1 and args[1].startswith("deal_"):
        deal_id = args[1].replace("deal_", "", 1)
        if deal_id in deals:
            deal = deals[deal_id]
            if deal["uid"] == uid:
                await message.answer(L(uid, "own_deal"), reply_markup=main_kb(uid))
                return

            buyer_name = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
            deal_text = L(uid, "deal_info",
                          deal_id=deal_id,
                          description=deal["description"],
                          amount=deal["amount"],
                          currency=deal["currency"])
            await message.answer(deal_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=L(uid, "btn_write_middle"), url=f"https://t.me/{MIDDLE_USERNAME.lstrip('@')}")],
                [InlineKeyboardButton(text=L(uid, "btn_menu"), callback_data="menu")]
            ]))
            try:
                seller_uid = deal["uid"]
                await bot.send_message(
                    seller_uid,
                    L(seller_uid, "partner_notified", deal_id=deal_id, buyer=buyer_name),
                    parse_mode="HTML"
                )
            except Exception:
                pass
        else:
            await message.answer(L(uid, "deal_not_found"), reply_markup=main_kb(uid))
        return

    await show_menu(message, uid)

# ===================== MENU =====================
@dp.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await state.clear()
    await safe_delete(callback.message)
    await show_menu(callback.message, uid)
    await callback.answer()

# ===================== LANGUAGE =====================
@dp.callback_query(F.data == "language")
async def cb_language(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "lang_choose"), parse_mode="HTML", reply_markup=language_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("setlang_"))
async def cb_setlang(callback: CallbackQuery):
    uid = callback.from_user.id
    lang_code = callback.data.replace("setlang_", "")
    get_user(uid)["lang"] = lang_code
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "lang_set"), parse_mode="HTML")
    await show_menu(callback.message, uid)
    await callback.answer()

# ===================== SECURITY =====================
@dp.callback_query(F.data == "security")
async def cb_security(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "security"), parse_mode="HTML",
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton(text=L(uid,"btn_menu"), callback_data="menu")]
                                   ]))
    await callback.answer()

# ===================== DEAL =====================
@dp.callback_query(F.data == "deal")
async def cb_deal(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "agreement"), parse_mode="HTML", reply_markup=agreement_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "confirm_agreement")
async def cb_confirm(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "deal_step1"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(Deal.partner)
    await callback.answer()

@dp.message(Deal.partner)
async def deal_partner(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    await safe_delete(message)
    text = message.text.strip()
    if not text.startswith("@"):
        await message.answer(L(uid, "invalid_username"), parse_mode="HTML", reply_markup=cancel_kb(uid))
        return
    await state.update_data(partner=text)
    await message.answer(L(uid, "deal_step2"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(Deal.description)

@dp.message(Deal.description)
async def deal_desc(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    await safe_delete(message)
    await state.update_data(description=message.text)
    await message.answer(L(uid, "deal_step3"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(Deal.amount)

@dp.message(Deal.amount)
async def deal_amt(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    await safe_delete(message)
    await state.update_data(amount=message.text)
    await message.answer(L(uid, "deal_step4"), parse_mode="HTML", reply_markup=currency_kb(uid))
    await state.set_state(Deal.currency)

@dp.callback_query(F.data.startswith("deal_cur_"))
async def deal_cur(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    cur_map = {
        "deal_cur_ton":   ("💎 TON",        "ton_wallet",     "ton"),
        "deal_cur_stars": ("⭐️ Stars",      "username_stars", "stars"),
        "deal_cur_card":  ("💳 Card (RUB)", "card",           "card"),
        "deal_cur_nft":   ("🎁 NFT",        None,             None),
    }
    cur_label, req_field, req_type = cur_map[callback.data]
    user = get_user(uid)

    if req_field and not user.get(req_field):
        await safe_delete(callback.message)
        await callback.message.answer(
            L(uid, "no_req", cur=cur_label),
            parse_mode="HTML", reply_markup=add_req_kb(uid, req_type)
        )
        await state.clear()
        await callback.answer()
        return

    data = await state.get_data()
    deal_id = gen_deal_id()
    deals[deal_id] = {
        "uid": uid,
        "partner": data.get("partner", "—"),
        "description": data.get("description", "—"),
        "amount": data.get("amount", "—"),
        "currency": cur_label,
        "status": "active"
    }
    user["deals_count"] = user.get("deals_count", 0) + 1

    me = await bot.get_me()
    deal_text = L(uid, "deal_created",
                  deal_id=deal_id,
                  partner=data.get("partner", "—"),
                  description=data.get("description", "—"),
                  amount=data.get("amount", "—"),
                  currency=cur_label,
                  bot_username=me.username)

    await safe_delete(callback.message)
    await callback.message.answer(deal_text, parse_mode="HTML", reply_markup=back_kb(uid))

    uname = f"@{callback.from_user.username}" if callback.from_user.username else f"ID: {uid}"
    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            f"🆕 <b>Новая сделка {deal_id}</b>\n\n👤 {uname} | ID: {uid}\n"
            f"👥 Партнёр: {data.get('partner','—')}\n"
            f"📋 {data.get('description','—')}\n💵 {data.get('amount','—')}\n💱 {cur_label}",
            parse_mode="HTML"
        )
    await state.clear()
    await callback.answer()

# ---- add req from deal flow ----
@dp.callback_query(F.data.endswith("_deal") & F.data.startswith("req_"))
async def req_from_deal(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    req_type = callback.data.replace("req_", "").replace("_deal", "")
    key_map = {"ton": "enter_ton", "card": "enter_card", "stars": "enter_stars"}
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, key_map[req_type]), parse_mode="HTML", reply_markup=cancel_kb(uid))
    state_map = {"ton": AddReq.ton, "card": AddReq.card, "stars": AddReq.stars}
    await state.set_state(state_map[req_type])
    await state.update_data(from_deal=True)
    await callback.answer()

# ===================== REQUISITES =====================
@dp.callback_query(F.data == "requisites")
async def cb_req(callback: CallbackQuery):
    uid = callback.from_user.id
    u = get_user(uid)
    text = L(uid, "req_title",
             ton=u.get("ton_wallet") or "—",
             card=u.get("card") or "—",
             stars=u.get("username_stars") or "—")
    await safe_delete(callback.message)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=req_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "req_ton")
async def cb_req_ton(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "enter_ton"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(AddReq.ton)
    await callback.answer()

@dp.callback_query(F.data == "req_card")
async def cb_req_card(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "enter_card"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(AddReq.card)
    await callback.answer()

@dp.callback_query(F.data == "req_stars")
async def cb_req_stars(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "enter_stars"), parse_mode="HTML", reply_markup=cancel_kb(uid))
    await state.set_state(AddReq.stars)
    await callback.answer()

@dp.message(AddReq.ton)
async def save_ton(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    get_user(uid).update({"ton_wallet": message.text, "has_requisites": True})
    data = await state.get_data()
    await safe_delete(message)
    await state.clear()
    suffix = L(uid, "redo_deal") if data.get("from_deal") else ""
    await message.answer(L(uid, "ton_saved") + suffix, parse_mode="HTML", reply_markup=main_kb(uid))

@dp.message(AddReq.card)
async def save_card(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    get_user(uid).update({"card": message.text, "has_requisites": True})
    data = await state.get_data()
    await safe_delete(message)
    await state.clear()
    suffix = L(uid, "redo_deal") if data.get("from_deal") else ""
    await message.answer(L(uid, "card_saved") + suffix, parse_mode="HTML", reply_markup=main_kb(uid))

@dp.message(AddReq.stars)
async def save_stars(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    get_user(uid).update({"username_stars": message.text, "has_requisites": True})
    data = await state.get_data()
    await safe_delete(message)
    await state.clear()
    suffix = L(uid, "redo_deal") if data.get("from_deal") else ""
    await message.answer(L(uid, "stars_saved") + suffix, parse_mode="HTML", reply_markup=main_kb(uid))

# ===================== TOPUP =====================
@dp.callback_query(F.data == "topup")
async def cb_topup(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "topup_title"), parse_mode="HTML", reply_markup=topup_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_stars")
async def cb_topup_stars(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "topup_stars"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_ton")
async def cb_topup_ton(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "topup_ton"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_card")
async def cb_topup_card(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "topup_card"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_nft")
async def cb_topup_nft(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "topup_nft"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

# ===================== WITHDRAW =====================
@dp.callback_query(F.data == "withdraw")
async def cb_withdraw(callback: CallbackQuery):
    uid = callback.from_user.id
    await safe_delete(callback.message)
    await callback.message.answer(L(uid, "withdraw_text"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

# ===================== ADMIN =====================
@dp.message(Command("adm"))
async def cmd_adm(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await safe_delete(message)
    total = len([k for k in user_data if not str(k).startswith("_")])
    await message.answer(
        f"🔧 <b>Админ-панель | Crypto Deals • Middle</b>\n\n"
        f"👥 Пользователей: <b>{total}</b>\n"
        f"📋 Сделок: <b>{len(deals)}</b>",
        parse_mode="HTML", reply_markup=admin_kb())

@dp.callback_query(F.data == "adm_banner")
async def adm_banner(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await safe_delete(callback.message)
    await callback.message.answer(
        "📸 Отправьте <b>фото + подпись (caption)</b> для нового баннера.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")]]))
    await state.set_state(SetBanner.waiting)
    await callback.answer()

@dp.message(SetBanner.waiting, F.photo)
async def save_banner(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    user_data["_banner"] = {"photo_id": message.photo[-1].file_id, "caption": message.caption or ""}
    await safe_delete(message)
    await message.answer("✅ Баннер обновлён!", reply_markup=admin_kb())
    await state.clear()

@dp.callback_query(F.data == "adm_stats")
async def adm_stats(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    total = len([k for k in user_data if not str(k).startswith("_")])
    with_req = len([v for k,v in user_data.items() if not str(k).startswith("_") and isinstance(v,dict) and v.get("has_requisites")])
    active = len([d for d in deals.values() if d.get("status") == "active"])
    await callback.message.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Всего: <b>{total}</b>\n"
        f"🧾 С реквизитами: <b>{with_req}</b>\n"
        f"📋 Сделок: <b>{len(deals)}</b>\n"
        f"🟢 Активных: <b>{active}</b>",
        parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_users")
async def adm_users(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    ulist = [k for k in user_data if not str(k).startswith("_")]
    text = f"👥 <b>Пользователи ({len(ulist)})</b>\n\n"
    for uid in ulist[:20]:
        u = user_data[uid]
        if not isinstance(u, dict): continue
        text += (f"• <code>{uid}</code> | ⭐{u.get('reputation',0)} | "
                 f"Сд:{u.get('deals_count',0)} | {'✅' if u.get('has_requisites') else '❌'} | {u.get('lang','ru')}\n")
    if len(ulist) > 20:
        text += f"\n...ещё {len(ulist)-20}"
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_reputation")
async def adm_rep(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "⭐️ <b>Выдача репутации</b>\n\nФормат: <code>@username +5</code> или <code>USER_ID -2</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")]]))
    await state.set_state(AdminAction.reputation)
    await callback.answer()

@dp.message(AdminAction.reputation)
async def process_rep(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    try:
        parts = message.text.strip().split()
        uid = find_uid(parts[0])
        if uid is None:
            await message.answer("❌ Пользователь не найден.", parse_mode="HTML")
            await state.clear()
            return
        delta = int(parts[1])
        user = get_user(uid)
        user["reputation"] = user.get("reputation", 0) + delta
        new_rep = user["reputation"]
        await message.answer(f"✅ Репутация <code>{uid}</code>: {delta:+}\nИтого: <b>{new_rep} ⭐</b>", parse_mode="HTML")
        await bot.send_message(uid, f"⭐️ Ваша репутация: <b>{delta:+}</b>\nТекущая: <b>{new_rep} ⭐</b>", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Формат: <code>@username +5</code>", parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == "adm_review")
async def adm_review(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "💬 <b>Добавить отзыв</b>\n\nФормат: <code>@username Текст</code> или <code>USER_ID Текст</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")]]))
    await state.set_state(AdminAction.review)
    await callback.answer()

@dp.message(AdminAction.review)
async def process_review(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    try:
        parts = message.text.strip().split(maxsplit=1)
        uid = find_uid(parts[0])
        if uid is None:
            await message.answer("❌ Пользователь не найден.", parse_mode="HTML")
            await state.clear()
            return
        review_text = parts[1]
        user = get_user(uid)
        user.setdefault("reviews", []).append(review_text)
        await message.answer(f"✅ Отзыв добавлен пользователю <code>{uid}</code>", parse_mode="HTML")
        await bot.send_message(uid, f"💬 <b>Новый отзыв:</b>\n\n{review_text}", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Формат: <code>@username Текст</code>", parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == "adm_balance")
async def adm_bal(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "💰 <b>Изменить баланс</b>\n\nФормат: <code>@username СУММА</code>\nПример: <code>@ivan 150.5</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")]]))
    await state.set_state(AdminAction.balance)
    await callback.answer()

@dp.message(AdminAction.balance)
async def process_bal(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    try:
        parts = message.text.strip().split()
        uid = find_uid(parts[0])
        if uid is None:
            await message.answer("❌ Пользователь не найден.", parse_mode="HTML")
            await state.clear()
            return
        amount = float(parts[1])
        user = get_user(uid)
        old = user.get("balance", 0)
        user["balance"] = amount
        await message.answer(f"✅ Баланс <code>{uid}</code>: {old} → <b>{amount}</b>", parse_mode="HTML")
        await bot.send_message(uid, f"💰 Ваш баланс обновлён: <b>{amount}</b>", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Формат: <code>@username СУММА</code>", parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == "adm_deals")
async def adm_deals_cb(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    if not deals:
        await callback.message.answer("📋 Сделок пока нет.")
        await callback.answer()
        return
    text = f"📋 <b>Сделки ({len(deals)})</b>\n\n"
    for deal_id, d in list(deals.items())[-10:]:
        text += (f"🆔 <code>{deal_id}</code> | 👤 {d['uid']} | 👥 {d.get('partner','—')}\n"
                 f"💵 {d['amount']} {d['currency']} | {d['description'][:20]}...\n"
                 f"🔘 {d['status']}\n\n")
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_cancel")
async def adm_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Отменено.", reply_markup=admin_kb())
    await callback.answer()

# ===================== MAIN =====================
async def main():
    print("✅ Crypto Deals Middle Bot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
