import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"ton_wallet": "", "card": "", "username_stars": "", "has_requisites": False,
                          "balance": 0.0, "reputation": 0, "deals_count": 0, "reviews": []}
    return user_data[uid]

def gen_deal_id():
    deal_counter[0] += 1
    return f"CD{deal_counter[0]}"

# ===================== STATES =====================
class SetBanner(StatesGroup):
    waiting = State()

class AddReq(StatesGroup):
    ton = State()
    card = State()
    stars = State()

class Deal(StatesGroup):
    description = State()
    amount = State()
    currency = State()

class AdminAction(StatesGroup):
    reputation = State()
    balance = State()
    review = State()

# username -> uid mapping (populated on every user message)
username_map = {}  # "username_lowercase" -> uid

def find_uid(query: str):
    """Find UID by @username or numeric ID"""
    q = query.strip()
    if q.startswith("@"):
        return username_map.get(q[1:].lower())
    try:
        uid = int(q)
        return uid if uid in user_data else None
    except ValueError:
        return None

# ===================== TEXTS =====================
WELCOME_TEXT = (
    "Добро пожаловать 👋\n\n"
    "💼 <b>Crypto Deals • Middle</b> - Мы специализированный сервис по обеспечению безопасности вне биржевых сделок.\n\n"
    "✨ Автоматизированный алгоритм исполнения.\n"
    "⚡️ Скорость и автоматизация.\n"
    "💳 Удобный и быстрый вывод средств.\n\n"
    "• Комиссия сервиса: <b>0%</b>\n"
    "• Режим работы: <b>24/7</b>\n"
    f"• Техническая поддержка: <b>{MIDDLE_USERNAME}</b>"
)

SECURITY_TEXT = (
    "🛡 <b>БЕЗОПАСНОСТЬ ПРИ ПЕРЕДАЧЕ АКТИВОВ</b>\n\n"
    "Для обеспечения сохранности ваших активов и исключения случаев мошенничества, "
    "проведение сделок осуществляется строго в соответствии со следующими правилами:\n\n"
    "<b>• Передача активов:</b>\n"
    f"Передача NFT-подарка или иных ценностей производится исключительно на официальный эскроу-аккаунт сервиса: <b>{MIDDLE_USERNAME}</b>\n\n"
    "<b>• Запрет прямых транзакций:</b>\n"
    "Категорически запрещается передача активов напрямую покупателю/продавцу. "
    "Сервис гарантирует исполнение обязательств только при условии проведения транзакции через официальный сервис.\n\n"
    "<b>• Верификация реквизитов:</b>\n"
    "Перед отправкой актива обязательно сверяйте итоговую сумму и уникальный идентификатор (тег) сделки, указанный в комментарии к платежу.\n\n"
    "<b>• Завершение операции:</b>\n"
    "Вывод средств/передача актива стороне-получателю производится автоматизированно после подтверждения обеими сторонами выполнения условий сделки."
)

AGREEMENT_TEXT = (
    "☑️ <b>Пользовательское соглашение</b>\n\n"
    "🛡️ Для обеспечения сохранности ваших активов строго соблюдайте установленный регламент:\n\n"
    "<b>• Депонирование активов:</b>\n"
    f"Передача активов осуществляется исключительно через официальный контакт: <b>{MIDDLE_USERNAME}</b>\n\n"
    "<b>• Запрет прямых расчетов:</b>\n"
    "Категорически запрещено отправлять средства или товары напрямую покупателю/продавцу.\n\n"
    "<b>• Завершение сделки:</b>\n"
    "Вывод средств продавцу производится автоматически после подтверждения покупателем получения товара/услуги.\n\n"
    "Подтверждая ознакомление, нажмите кнопку ниже."
)

# ===================== KEYBOARDS =====================
def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Создать Сделку", callback_data="deal"),
         InlineKeyboardButton(text="🧾 Реквизиты", callback_data="requisites")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="topup"),
         InlineKeyboardButton(text="💸 Вывести средства", callback_data="withdraw")],
        [InlineKeyboardButton(text="🛡 Безопасность", callback_data="security"),
         InlineKeyboardButton(text="📋 Поддержка", url="https://t.me/CryptoDeal_Middle")],
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 В меню", callback_data="menu")],
        [InlineKeyboardButton(text="📋 Поддержка", url="https://t.me/CryptoDeal_Middle")],
    ])

def cancel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="menu")]
    ])

def agreement_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Подтвердить Ознакомление", callback_data="confirm_agreement")],
        [InlineKeyboardButton(text="📱 Вернуться в меню", callback_data="menu")],
        [InlineKeyboardButton(text="📋 Поддержка", url="https://t.me/CryptoDeal_Middle")],
    ])

def currency_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON", callback_data="deal_cur_ton"),
         InlineKeyboardButton(text="⭐️ Stars", callback_data="deal_cur_stars")],
        [InlineKeyboardButton(text="💳 Карта (RUB)", callback_data="deal_cur_card"),
         InlineKeyboardButton(text="🎁 NFT", callback_data="deal_cur_nft")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="menu")],
    ])

def req_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 TON кошелёк", callback_data="req_ton"),
         InlineKeyboardButton(text="💳 Карта", callback_data="req_card")],
        [InlineKeyboardButton(text="⭐️ Username для Stars", callback_data="req_stars")],
        [InlineKeyboardButton(text="📱 В меню", callback_data="menu")],
    ])

def add_req_kb(req_type):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить реквизит", callback_data=f"req_{req_type}_deal")],
        [InlineKeyboardButton(text="📗 В меню", callback_data="menu")],
    ])

def topup_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐️ Stars", callback_data="topup_stars"),
         InlineKeyboardButton(text="💎 TON", callback_data="topup_ton")],
        [InlineKeyboardButton(text="💳 Карта", callback_data="topup_card"),
         InlineKeyboardButton(text="🎁 NFT", callback_data="topup_nft")],
        [InlineKeyboardButton(text="📱 В меню", callback_data="menu")],
        [InlineKeyboardButton(text="📋 Поддержка", url="https://t.me/CryptoDeal_Middle")],
    ])

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Изменить баннер", callback_data="adm_banner"),
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

async def show_menu(message: Message):
    banner = user_data.get("_banner")
    if banner:
        await message.answer_photo(photo=banner["photo_id"],
                                   caption=banner.get("caption") or WELCOME_TEXT,
                                   parse_mode="HTML", reply_markup=main_kb())
    else:
        await message.answer(WELCOME_TEXT, parse_mode="HTML", reply_markup=main_kb())

# ===================== /START =====================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    uid = message.from_user.id
    get_user(uid)
    if message.from_user.username:
        username_map[message.from_user.username.lower()] = uid
    await safe_delete(message)
    await show_menu(message)

def _reg(msg: Message):
    if msg.from_user and msg.from_user.username:
        username_map[msg.from_user.username.lower()] = msg.from_user.id

# ===================== MENU =====================
@dp.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_delete(callback.message)
    await show_menu(callback.message)
    await callback.answer()

# ===================== SECURITY =====================
@dp.callback_query(F.data == "security")
async def cb_security(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(SECURITY_TEXT, parse_mode="HTML",
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton(text="📱 В меню", callback_data="menu")]
                                   ]))
    await callback.answer()

# ===================== DEAL =====================
@dp.callback_query(F.data == "deal")
async def cb_deal(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(AGREEMENT_TEXT, parse_mode="HTML", reply_markup=agreement_kb())
    await callback.answer()

@dp.callback_query(F.data == "confirm_agreement")
async def cb_confirm(callback: CallbackQuery, state: FSMContext):
    await safe_delete(callback.message)
    await callback.message.answer(
        "📝 <b>Создание сделки — Шаг 1/3</b>\n\nВведите <b>суть сделки</b> (что продаёте/покупаете):",
        parse_mode="HTML", reply_markup=cancel_kb()
    )
    await state.set_state(Deal.description)
    await callback.answer()

@dp.message(Deal.description)
async def deal_desc(message: Message, state: FSMContext):
    _reg(message)
    await safe_delete(message)
    await state.update_data(description=message.text)
    await message.answer(
        "📝 <b>Создание сделки — Шаг 2/3</b>\n\nВведите <b>сумму сделки</b>:",
        parse_mode="HTML", reply_markup=cancel_kb()
    )
    await state.set_state(Deal.amount)

@dp.message(Deal.amount)
async def deal_amt(message: Message, state: FSMContext):
    _reg(message)
    await safe_delete(message)
    await state.update_data(amount=message.text)
    await message.answer(
        "📝 <b>Создание сделки — Шаг 3/3</b>\n\nВ чём хотите получить оплату?",
        parse_mode="HTML", reply_markup=currency_kb()
    )
    await state.set_state(Deal.currency)

@dp.callback_query(F.data.startswith("deal_cur_"))
async def deal_cur(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    cur_map = {
        "deal_cur_ton":   ("💎 TON",        "ton_wallet",     "ton"),
        "deal_cur_stars": ("⭐️ Stars",      "username_stars", "stars"),
        "deal_cur_card":  ("💳 Карта (RUB)","card",           "card"),
        "deal_cur_nft":   ("🎁 NFT",        None,             None),
    }
    cur_label, req_field, req_type = cur_map[callback.data]
    user = get_user(uid)

    if req_field and not user.get(req_field):
        await safe_delete(callback.message)
        await callback.message.answer(
            f"📎 Вы не добавили реквизит для получения <b>{cur_label}</b>.\n\n"
            "Сначала добавьте реквизит, затем создайте сделку снова.",
            parse_mode="HTML", reply_markup=add_req_kb(req_type)
        )
        await state.clear()
        await callback.answer()
        return

    data = await state.get_data()
    deal_id = gen_deal_id()
    deals[deal_id] = {"uid": uid, "description": data.get("description","—"),
                      "amount": data.get("amount","—"), "currency": cur_label, "status": "active"}
    user["deals_count"] = user.get("deals_count", 0) + 1

    me = await bot.get_me()
    deal_text = (
        f"✅ <b>Сделка создана!</b>\n\n"
        f"🆔 ID сделки: <code>{deal_id}</code>\n"
        f"📋 Суть: {data.get('description','—')}\n"
        f"💵 Сумма: {data.get('amount','—')}\n"
        f"💱 Валюта: {cur_label}\n"
        f"🔗 Ссылка: <code>https://t.me/{me.username}?start=deal_{deal_id}</code>\n\n"
        f"📦 <b>Товар передавать на: {MIDDLE_USERNAME}</b>\n\n"
        f"⏳ Статус: <b>Активна</b>"
    )
    await safe_delete(callback.message)
    await callback.message.answer(deal_text, parse_mode="HTML", reply_markup=back_kb())

    uname = f"@{callback.from_user.username}" if callback.from_user.username else f"ID: {uid}"
    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            f"🆕 <b>Новая сделка {deal_id}</b>\n\n👤 {uname} | ID: {uid}\n"
            f"📋 {data.get('description','—')}\n💵 {data.get('amount','—')}\n💱 {cur_label}",
            parse_mode="HTML"
        )
    await state.clear()
    await callback.answer()

# ---- add req from deal flow ----
@dp.callback_query(F.data.endswith("_deal") & F.data.startswith("req_"))
async def req_from_deal(callback: CallbackQuery, state: FSMContext):
    req_type = callback.data.replace("req_", "").replace("_deal", "")
    labels = {"ton": "💎 TON кошелёк", "card": "💳 номер карты", "stars": "⭐️ username для Stars"}
    await safe_delete(callback.message)
    await callback.message.answer(f"Введите {labels.get(req_type, 'реквизит')}:", parse_mode="HTML", reply_markup=cancel_kb())
    state_map = {"ton": AddReq.ton, "card": AddReq.card, "stars": AddReq.stars}
    await state.set_state(state_map[req_type])
    await state.update_data(from_deal=True)
    await callback.answer()

# ===================== REQUISITES =====================
@dp.callback_query(F.data == "requisites")
async def cb_req(callback: CallbackQuery):
    uid = callback.from_user.id
    u = get_user(uid)
    text = (
        "🧾 <b>Реквизиты</b>\n\n"
        f"💎 TON: <code>{u.get('ton_wallet') or '—'}</code>\n"
        f"💳 Карта: <code>{u.get('card') or '—'}</code>\n"
        f"⭐️ Stars username: <code>{u.get('username_stars') or '—'}</code>"
    )
    await safe_delete(callback.message)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=req_kb())
    await callback.answer()

@dp.callback_query(F.data == "req_ton")
async def cb_req_ton(callback: CallbackQuery, state: FSMContext):
    await safe_delete(callback.message)
    await callback.message.answer("💎 Введите ваш <b>TON кошелёк</b>:", parse_mode="HTML", reply_markup=cancel_kb())
    await state.set_state(AddReq.ton)
    await callback.answer()

@dp.callback_query(F.data == "req_card")
async def cb_req_card(callback: CallbackQuery, state: FSMContext):
    await safe_delete(callback.message)
    await callback.message.answer("💳 Введите <b>номер карты</b>:", parse_mode="HTML", reply_markup=cancel_kb())
    await state.set_state(AddReq.card)
    await callback.answer()

@dp.callback_query(F.data == "req_stars")
async def cb_req_stars(callback: CallbackQuery, state: FSMContext):
    await safe_delete(callback.message)
    await callback.message.answer("⭐️ Введите ваш <b>Telegram username</b> для получения Stars:", parse_mode="HTML", reply_markup=cancel_kb())
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
    suffix = "\n\nТеперь создайте сделку заново." if data.get("from_deal") else ""
    await message.answer(f"✅ TON кошелёк сохранён!{suffix}", parse_mode="HTML", reply_markup=main_kb())

@dp.message(AddReq.card)
async def save_card(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    get_user(uid).update({"card": message.text, "has_requisites": True})
    data = await state.get_data()
    await safe_delete(message)
    await state.clear()
    suffix = "\n\nТеперь создайте сделку заново." if data.get("from_deal") else ""
    await message.answer(f"✅ Карта сохранена!{suffix}", parse_mode="HTML", reply_markup=main_kb())

@dp.message(AddReq.stars)
async def save_stars(message: Message, state: FSMContext):
    uid = message.from_user.id
    _reg(message)
    get_user(uid).update({"username_stars": message.text, "has_requisites": True})
    data = await state.get_data()
    await safe_delete(message)
    await state.clear()
    suffix = "\n\nТеперь создайте сделку заново." if data.get("from_deal") else ""
    await message.answer(f"✅ Username для Stars сохранён!{suffix}", parse_mode="HTML", reply_markup=main_kb())

# ===================== TOPUP =====================
@dp.callback_query(F.data == "topup")
async def cb_topup(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer("💰 <b>Пополнение баланса</b>\n\nВыберите способ:", parse_mode="HTML", reply_markup=topup_kb())
    await callback.answer()

@dp.callback_query(F.data == "topup_stars")
async def cb_topup_stars(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(
        f"⭐️ <b>Пополнение баланса посредством Telegram Stars:</b>\n\n"
        f"Для зачисления необходимо передать Stars на: <b>{MIDDLE_USERNAME}</b>\n\n"
        f"• Перейдите в диалог: <b>{MIDDLE_USERNAME}</b>\n"
        f"• Используйте функционал Telegram для отправки Stars.\n"
        f"• После подтверждения баланс будет пополнен автоматически.\n\n"
        f"⚠️ Совершайте перевод исключительно по указанным реквизитам.\n\n"
        f"⏱ Зачисление: <b>5–15 минут</b>",
        parse_mode="HTML", reply_markup=back_kb())
    await callback.answer()

@dp.callback_query(F.data == "topup_ton")
async def cb_topup_ton(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(
        f"💎 <b>Адрес для зачисления TON:</b>\n\n<code>{TON_ADDRESS}</code>\n\n"
        f"По факту отправки обратитесь в поддержку: <b>{MIDDLE_USERNAME}</b>\n\n"
        f"⏱ Зачисление: <b>5–15 минут</b>",
        parse_mode="HTML", reply_markup=back_kb())
    await callback.answer()

@dp.callback_query(F.data == "topup_card")
async def cb_topup_card(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(
        f"💳 <b>Пополнение баланса: Банковские карты (РФ)</b>\n\n"
        f"Реквизиты для перевода:\n<code>{CARD_NUMBER}</code>\n"
        f"{CARD_BANK}\n\n"
        f"• Сохраните чек транзакции.\n"
        f"• Обратитесь в поддержку для подтверждения.\n\n"
        f"⏱ Зачисление: <b>5–15 минут</b>",
        parse_mode="HTML", reply_markup=back_kb())
    await callback.answer()

@dp.callback_query(F.data == "topup_nft")
async def cb_topup_nft(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(
        f"🎁 <b>Пополнение посредством NFT</b>\n\n"
        f"Принимаем любые лимитированные подарки из коллекции Telegram.\n\n"
        f"• Передайте актив: <b>{MIDDLE_USERNAME}</b>\n"
        f"• После верификации будет произведена оценка в Stars или TON.\n\n"
        f"⏱ Зачисление: <b>5–15 минут</b>",
        parse_mode="HTML", reply_markup=back_kb())
    await callback.answer()

# ===================== WITHDRAW =====================
@dp.callback_query(F.data == "withdraw")
async def cb_withdraw(callback: CallbackQuery):
    await safe_delete(callback.message)
    await callback.message.answer(
        f"💸 <b>Вывод средств</b>\n\n"
        f"Для вывода средств обратитесь в поддержку:\n👤 {MIDDLE_USERNAME}\n\n"
        f"⚠️ Укажите сумму и реквизиты для вывода.",
        parse_mode="HTML", reply_markup=back_kb())
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
        "📸 Отправьте <b>фото + подпись (caption)</b> одним сообщением для нового баннера.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")]]))
    await state.set_state(SetBanner.waiting)
    await callback.answer()

@dp.message(SetBanner.waiting, F.photo)
async def save_banner(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    user_data["_banner"] = {"photo_id": message.photo[-1].file_id, "caption": message.caption or WELCOME_TEXT}
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
        f"👥 Всего пользователей: <b>{total}</b>\n"
        f"🧾 С реквизитами: <b>{with_req}</b>\n"
        f"📋 Всего сделок: <b>{len(deals)}</b>\n"
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
                 f"Сд:{u.get('deals_count',0)} | {'✅' if u.get('has_requisites') else '❌'}\n")
    if len(ulist) > 20:
        text += f"\n...ещё {len(ulist)-20}"
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "adm_reputation")
async def adm_rep(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "⭐️ <b>Выдача репутации</b>\n\n"
        "Формат: <code>@username +5</code> или <code>USER_ID -2</code>",
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
            await message.answer("❌ Пользователь не найден. Убедитесь что он писал боту.", parse_mode="HTML")
            await state.clear()
            return
        delta = int(parts[1])
        user = get_user(uid)
        user["reputation"] = user.get("reputation", 0) + delta
        new_rep = user["reputation"]
        await message.answer(f"✅ Репутация <code>{uid}</code>: {delta:+}\nИтого: <b>{new_rep} ⭐</b>", parse_mode="HTML")
        await bot.send_message(uid, f"⭐️ Ваша репутация изменена на <b>{delta:+}</b>\nТекущая: <b>{new_rep} ⭐</b>", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Формат: <code>@username +5</code> или <code>USER_ID +5</code>", parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == "adm_review")
async def adm_review(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "💬 <b>Добавить отзыв</b>\n\nФормат: <code>@username Текст отзыва</code> или <code>USER_ID Текст</code>",
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
        await bot.send_message(uid, f"💬 <b>Новый отзыв о вашей сделке:</b>\n\n{review_text}", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Формат: <code>@username Текст</code>", parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == "adm_balance")
async def adm_bal(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer(
        "💰 <b>Изменить баланс</b>\n\nФормат: <code>@username СУММА</code> или <code>USER_ID СУММА</code>\nПример: <code>@ivan 150.5</code>",
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
        text += (f"🆔 <code>{deal_id}</code> | 👤 {d['uid']}\n"
                 f"💵 {d['amount']} {d['currency']} | {d['description'][:25]}...\n"
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
