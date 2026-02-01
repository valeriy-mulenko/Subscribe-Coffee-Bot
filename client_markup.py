from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import Database

db = Database('database.db')


def get_client_keyboard():
    buttons = [
        [
            KeyboardButton(text="Профиль"),
            KeyboardButton(text="Подписка")
        ],
        [
            KeyboardButton(text="Тг канал"),
            KeyboardButton(text="Получить кофе")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def profile_keyboard():
    buttons = [
        [
            KeyboardButton(text="Назад")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_inline_sub(user_id):
    buttons = [
        [
            InlineKeyboardButton(text=f"{db.get_price(user_id)} ₽", callback_data="sub_month")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_profile():
    buttons = [
        [
            InlineKeyboardButton(text="Статус подписки", callback_data="client_substatus"),
            InlineKeyboardButton(text="Изменить имя", callback_data="client_changenickname")
        ], [
            InlineKeyboardButton(text="Назад⬅️", callback_data="client_back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_order():
    buttons = [
        [
            InlineKeyboardButton(text="Комментарий к заказу", callback_data="client_comment"),
            InlineKeyboardButton(text="Назад⬅️", callback_data="client_back")
        ], [
            InlineKeyboardButton(text="Получить кофе", callback_data="client_freecoffee")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_chanel():
    buttons = [
        [
            InlineKeyboardButton(text="Subscribe Coffee", url="https://t.me/subscribe_coffee")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
