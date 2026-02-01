from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_keyboard():
    buttons = [
        [
            KeyboardButton(text="Профиль")
        ], [
            KeyboardButton(text="Найти клиента")
        ], [
            KeyboardButton(text="Отправить стикер"),  # Рассылка клиентам стикеров
            KeyboardButton(text="Отправить сообщение")  # Рассылка клиентам сообщения
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_order_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Выдать кофе", callback_data="admin_successful"),
            InlineKeyboardButton(text="Отмена", callback_data="admin_cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_admin_client_profile():
    buttons = [
        [
            InlineKeyboardButton(text="Подписка за 3 890 ₽", callback_data="admin_sub"),
            InlineKeyboardButton(text="Подписка за 3 490 ₽", callback_data="admin_substudent"),
        ], [
            InlineKeyboardButton(text="Выдать бесплатную подписку", callback_data="admin_subfree"),
            InlineKeyboardButton(text="Назад⬅️", callback_data="client_back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_sticker():
    buttons = [
        [
            InlineKeyboardButton(text="Назад⬅️", callback_data="client_back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
