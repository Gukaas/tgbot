import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

BOT_TOKEN = '7768406433:AAEFIa_06d-EfHHKXH15r19bgBxCrqYVkdE'  # ← сюда вставь свой токен
ADMIN_ID = 1033527214      # ← сюда свой Telegram ID
YM_ACCOUNT = '4100118160340772'
PARTNER_LINK = 'https://1wbfqv.life/?open=register&p=3thr'
CRYPTO_LINK = 'https://t.me/send?start=IV2ZeQGxBqSu'

referrals = {}
discounts = {}

bot = telebot.TeleBot(BOT_TOKEN)

def main_menu(user_id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🛒 Купить", callback_data="buy"))
    markup.row(
        InlineKeyboardButton("🎁 Бесплатные прогнозы", callback_data="free_trial"),
        InlineKeyboardButton("🎟 Реф. ссылка", callback_data="ref_link")
    )
    markup.row(InlineKeyboardButton("📞 Поддержка", url="https://t.me/Poderska_admi"))
    return markup

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    args = msg.text.split()
    if len(args) > 1:
        inviter_id = int(args[1])
        if inviter_id != user_id and user_id not in referrals:
            referrals[user_id] = inviter_id
            discounts[inviter_id] = discounts.get(inviter_id, 0) + 1
            try:
                bot.send_message(inviter_id,
                    "🎉 По вашей ссылке зарегистрировался новый пользователь!\n"
                    "💸 Ваша скидка увеличена на 500₽.")
            except:
                pass

    text = (
        "👋 Добро пожаловать в *Penalty Mind AI*!\n\n"
        "🧠 *Описание:*\n"
        "ИИ-программа для прогнозов в игре Penalty Shoot-Out.\n\n"
        "📦 Внутри:\n"
        "• ИИ-модель\n• Интерфейс\n• Инструкция\n• Активация\n\n"
        "🎁 Или получите 3 прогноза бесплатно — кнопка внизу."
    )
    bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "buy")
def show_payment_options(call):
    user_id = call.from_user.id
    discount_count = discounts.get(user_id, 0)
    discount = discount_count * 500
    final_amount = max(1000, 8900 - discount)

    ym_link = (
        f"https://yoomoney.ru/quickpay/shop-widget?"
        f"writer=seller&targets=Penalty+Mind+AI&default-sum={final_amount}"
        f"&button-text=14&payment-type-choice=on&hint=&successURL=&account={YM_ACCOUNT}"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(f"💳 ЮMoney ({final_amount}₽)", url=ym_link),
        InlineKeyboardButton("💰 CryptoBot", url=CRYPTO_LINK)
    )
    markup.row(InlineKeyboardButton("✅ Я оплатил", callback_data="check_payment"))
    markup.add(InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu"))

    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        f"💸 Ваша скидка: {discount}₽\n💰 К оплате: {final_amount}₽",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_payment")
def check_payment(call):
    user = call.from_user
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = (
        f"📥 Пользователь нажал 'Я оплатил':\n"
        f"Имя: {user.first_name}\n"
        f"Юзернейм: @{user.username}\n"
        f"ID: {user.id}\n"
        f"⏰ Время: {dt}"
    )
    bot.send_message(ADMIN_ID, msg)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "✅ Спасибо! Мы проверим оплату и пришлём ссылку на программу.", reply_markup=main_menu(user.id))

@bot.callback_query_handler(func=lambda call: call.data == "free_trial")
def free_trial(call):
    bot.answer_callback_query(call.id)
    text = (
        "📲 Чтобы получить *3 бесплатных прогноза*:\n\n"
        "1️⃣ Зарегистрируйтесь на 1win по ссылке ниже.\n"
        "2️⃣ Аккаунт должен быть *новым*.\n"
        "3️⃣ Пополните баланс на *любую сумму*.\n\n"
        f"🔗 [РЕГИСТРАЦИЯ]({PARTNER_LINK})\n\n"
        "✅ После выполнения нажмите кнопку ниже."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 РЕГИСТРАЦИЯ", url=PARTNER_LINK))
    markup.add(InlineKeyboardButton("✅ Я выполнил условия", callback_data="check_trial"))
    markup.add(InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_trial")
def check_trial(call):
    user = call.from_user
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = (
        f"🎁 Пользователь запросил бесплатные прогнозы:\n"
        f"Имя: {user.first_name}\n"
        f"Юзернейм: @{user.username}\n"
        f"ID: {user.id}\n"
        f"⏰ Время: {dt}"
    )
    bot.send_message(ADMIN_ID, msg)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "🔍 Мы проверим выполнение условий и пришлём доступ к прогнозам.", reply_markup=main_menu(user.id))

@bot.callback_query_handler(func=lambda call: call.data == "ref_link")
def send_ref_link(call):
    user_id = call.from_user.id
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    count = discounts.get(user_id, 0)
    discount = count * 500
    text = (
        f"🎟 Ваша реферальная ссылка:\n{ref_link}\n\n"
        f"👥 Приглашено: {count}\n"
        f"💸 Скидка: {discount}₽"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu"))
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "🔘 Главное меню", reply_markup=main_menu(call.from_user.id))

bot.infinity_polling()
