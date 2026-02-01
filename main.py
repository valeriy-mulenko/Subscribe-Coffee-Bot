import asyncio
import logging
import time
import datetime
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from dotenv import load_dotenv
from db import Database
import client_markup as nav
import admin_markup as adm

logging.basicConfig(level=logging.INFO)

load_dotenv()

YOOTOKEN = os.getenv("YOOTOKEN")
bot = Bot(os.getenv("BOT_TOKEN"))

dp = Dispatcher()

db = Database('database.db')
admin_id = os.getenv("ADMIN_ID")


def days_to_second(days):   # Количество дней подписки в секундах
    return days * 86400  # 1 day == 86400


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt


@dp.message(Command('start'))
async def start_command(message: types.Message):
    user_id = message.from_user.id

    if not db.user_exists(user_id):     # Регистрация клиента
        db.add_user(user_id)
        db.set_tg_name(user_id, f"@{message.chat.username}")
        await bot.send_message(user_id, "Как вас зовут?")
    else:
        if user_id == admin_id:
            reply_markup = adm.get_admin_keyboard()  # Выдача админ панели
        else:
            reply_markup = nav.get_client_keyboard()
        await bot.send_message(user_id, "Вы уже зарегистрированы!", reply_markup=reply_markup)


@dp.message(F.successful_payment)  # Обработка платежа
async def process_pay(message: types.Message):
    user_id = message.from_user.id

    db.set_telegram_payment_charge_id(user_id, message.successful_payment.telegram_payment_charge_id)  # Сохранение оплаты в бд
    db.set_provider_payment_charge_id(user_id, message.successful_payment.provider_payment_charge_id)

    if message.successful_payment.invoice_payload == "sub_month":   # Выдача подписки
        time_sub = int(time.time()) + days_to_second(30)    # Время окончания подписки (в секундах)

        db.set_time_sub(user_id, time.strftime("%d.%m.%Y, %H:%M:%S"))   # Время выдачи подписки
        db.set_end_of_sub(user_id, time_sub)
        db.set_type_sub(user_id, "30 дней")
        db.set_coffee_today(user_id, "Есть ✅")

        await bot.send_message(user_id, "Подписка на 30 дней оформлена!")


@dp.message()  # MESSAGE
async def bot_message(message: types.Message):
    user_id = message.from_user.id

    if message.chat.type == 'private':

        if db.get_time_update_status(1):        # UPDATE COFFEE TODAY

            while int(db.get_time_update(1)) <= int(time.time()):   # Проверка для обновления нового дня подписки
                db.set_time_update(1, int(db.get_time_update(1)) + 86400)

            for row in db.get_users():
                db.set_coffee_today(row[0], "Есть ✅")

        if message.text == 'Подписка':
            if db.get_price(user_id) == "3490":
                await bot.send_message(user_id, "Подписка на 30 дней (Студенческая)",
                                       reply_markup=nav.get_inline_sub(user_id))
            else:
                await bot.send_message(user_id, "Подписка на 30 дней", reply_markup=nav.get_inline_sub(user_id))

        elif message.text == 'Найти клиента':
            if user_id == admin_id:
                await bot.send_message(user_id, "Отправьте ник клиента как в профиле тг через @")
                db.set_status(1, "student")

        elif message.text == 'Отправить стикер':
            if user_id == admin_id:
                await bot.send_message(user_id, "Какой стикер отправить?", reply_markup=adm.get_sticker())
                db.set_status(1, "sticker")

        elif message.text == 'Отправить сообщение':
            if user_id == admin_id:
                await bot.send_message(user_id, "Какое сообщение отправить?", reply_markup=adm.get_sticker())
                db.set_status(1, "text")
            else:
                pass

        elif message.text == "Получить кофе":

            if db.get_sub_status(user_id):  # Проверка на активность подписки
                if db.get_coffee_today(user_id) == "Есть ✅":    # Проверка на доступный сегодня кофе
                    await bot.send_message(user_id, "Сделать заказ или получить кофе",
                                           reply_markup=nav.get_inline_order())   # Продолжение оформления заказа черер инлайн кнопки

                else:
                    next_coffee = int(db.get_time_update(1)) - int(time.time())  # Время до обновления дня подписки
                    await bot.send_message(user_id,
                                           f"Следующий кофе по подписке можно получить через: {str(datetime.timedelta(seconds=next_coffee))}")
            else:
                await bot.send_message(user_id, "У вас нет подписки", reply_markup=nav.get_inline_sub(user_id))

        elif message.text == 'Профиль':     # Профиль клиента (кнопки: Статус подписки, Изменить имя)
            await bot.send_message(user_id, "Ваш профиль", reply_markup=nav.get_inline_profile())

        elif message.text == "Тг канал":    # Ссылка на канал кофейни
            await bot.send_message(user_id, "Наш телеграм канал", reply_markup=nav.get_inline_chanel())

        else:       # Обработка действий клиента
            if db.get_action(user_id) == "setnickname":  # Регистрация имени клиента
                if len(message.text) > 30:
                    await bot.send_message(user_id, "Имя не должно превышать 30 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(user_id, "Имя не должно содержать следующие символы: @ или /")
                else:
                    db.set_nickname(user_id, message.text)
                    db.set_signup(user_id, "done")

                    if user_id == admin_id:
                        reply_markup = adm.get_admin_keyboard()
                    else:
                        reply_markup = nav.get_client_keyboard()
                    await bot.send_message(user_id,
                                           f"Здравствуйте {db.get_nickname(user_id)}!",
                                           reply_markup=reply_markup)

            if db.get_action(user_id) == "changenickname":    # Изменение имени клиента
                if len(message.text) > 30:
                    await bot.send_message(user_id, "Имя не должно превышать 30 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(user_id, "Имя не должно содержать следующие символы: @ или /")
                else:
                    db.set_nickname(user_id, message.text)
                    db.set_signup(user_id, "done")

                    if user_id == admin_id:
                        reply_markup = adm.get_admin_keyboard()
                    else:
                        reply_markup = nav.get_client_keyboard()
                    await bot.send_message(user_id,
                                           f"Ваше имя изменено на {db.get_nickname(user_id)}",
                                           reply_markup=reply_markup)

            if db.get_action(user_id) == "comment":     # Обработка комментария клиента для заказа
                if len(message.text) > 200:
                    await bot.send_message(user_id, "Комментарий не должен превышать 200 символов")
                else:
                    db.set_comment(user_id, message.text)
                    db.set_signup(user_id, "done")
                    await bot.send_message(admin_id,
                                           f"{db.get_tg_name(user_id)}: {db.get_comment(user_id)}")
                    await bot.send_message(user_id, "Комментарий отправлен✅")

            # Далее обработка действий админа

            if db.get_status(1) == "student":       # Выдача клиенту статуса студент
                db.set_student(1, message.text)
                db.set_status(1, "done")
                user = False
                for row in db.get_users_tg_name():
                    if row[0].lower() == db.get_student(1).lower():
                        user = True
                        db.set_student(1, row[0])
                        await bot.send_message(admin_id, f"Клиент {db.get_student(1)}",
                                               reply_markup=adm.get_admin_client_profile())

                if not user:
                    await bot.send_message(admin_id, f"Клиент {db.get_student(1)} не найден ❌")

            if db.get_status(1) == "sticker":   # Запись в бд id стикера для рассылки
                db.set_sticker(1, message.sticker.file_id)
                db.set_status(1, "done")
                for row in db.get_users():
                    await bot.send_sticker(row[0], db.get_sticker(1))

            if db.get_status(1) == "text":  # Запись в бд текста для рассылки
                db.set_text(1, message.text)
                db.set_status(1, "done")
                for row in db.get_users():
                    await bot.send_message(row[0], db.get_text(1))


@dp.callback_query(F.data.startswith("admin_"))     # ADMIN PANEL
async def callbacks_result(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    user_id = ''.join(c if c.isdigit() else ' ' for c in callback.message.text).split()     # Получаем из сообщения id клиента

    if action == "successful":          # Выдача кофе по подписке клиенту
        db.set_coffee_today(user_id[0], "Нет ❌")        # Меняем статус в бд на сегодня как получено
        await callback.message.edit_text(f"Клиент {db.get_tg_name(user_id[0])} получил кофе по подписке")
        await bot.send_message(user_id[0], "Хорошего дня! Ждём вас снова!")

    elif action == "sub":               # Обычная подписка
        db.set_price_tg_name(db.get_student(1), 3890)
        user_id = db.get_user_id(db.get_student(1))
        await callback.message.edit_text(
            f"Клиенту {db.get_student(1)} установлена цена {db.get_price_tg_name(db.get_student(1))}") # Сообщение для админа
        await bot.send_message(user_id, f"Теперь для вас стоимость подписки {db.get_price(user_id)} ₽") # Сообщение для клиента

    elif action == "substudent":        # Студенческая подписка
        db.set_price_tg_name(db.get_student(1), 3490)   # Обновление цены на студенческую
        user_id = db.get_user_id(db.get_student(1))

        await callback.message.edit_text(
            f"Клиенту {db.get_student(1)} установлена цена {db.get_price_tg_name(db.get_student(1))}") # Сообщение для админа
        await bot.send_message(user_id, f"Теперь для вас стоимость подписки {db.get_price(user_id)} ₽") # Сообщение для клиента

    elif action == "subfree":           # Выдача бесплатной подписки
        user_id = db.get_user_id(db.get_student(1))

        time_sub = int(time.time()) + days_to_second(30)
        db.set_time_sub(user_id, time.strftime("%d.%m.%Y, %H:%M:%S"))
        db.set_end_of_sub(user_id, time_sub)
        db.set_type_sub(user_id, "30 дней (Бесплатная)")
        db.set_coffee_today(user_id, "Есть ✅")
        await callback.message.edit_text(
            f"Клиенту {db.get_student(1)} выдана бесплатная подписка")
        await bot.send_message(user_id, "Теперь у вас есть подписка на 30 дней!")

    elif action == "sticker":
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.send_message(callback.message.chat.id, "Какой стикер отправить?", reply_markup=adm.get_sticker())
    elif action == "cancel":
        await callback.message.edit_text("Отмена ✅")
    else:
        await callback.message.edit_text("Ошибка при получении ответа")
    await callback.answer()


@dp.callback_query(F.data.startswith("client_"))  # CLIENT
async def callbacks_result(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    client_id = callback.message.chat.id

    if action == "freecoffee":     # Отправка заказа бариста
        if db.get_coffee_today(client_id) == "Есть ✅":

            keyboard = adm.get_order_keyboard()
            await bot.send_message(admin_id, f"id: {db.get_user_id_for_order(client_id)} \n"
                                             f"Имя: {db.get_nickname(client_id)} \n"
                                             f"Ник в тг: {db.get_tg_name(client_id)}\n"
                                             f"Последняя подписка: {str(db.get_time_sub(client_id))}\n"
                                             f"Кофе по подписке: {db.get_coffee_today(client_id)}\n"
                                             f"Тип подписки: 30",
                                   reply_markup=keyboard)

            await callback.message.edit_text("☕️")
        else:
            next_coffee = int(db.get_time_update(1)) - int(time.time())
            await bot.send_message(client_id,
                                   f"Следующий кофе по подписке можно получить через: {str(datetime.timedelta(seconds=next_coffee))}")

    elif action == "comment":       # Отправка заказа с комментарием бариста
        if db.get_coffee_today(client_id) == "Есть ✅":

            keyboard = adm.get_order_keyboard()
            await bot.send_message(admin_id, f"id: {db.get_user_id_for_order(client_id)} \n"
                                             f"Имя: {db.get_nickname(client_id)} \n"
                                             f"Ник в тг: {db.get_tg_name(client_id)}\n"
                                             f"Последняя подписка: {str(db.get_time_sub(client_id))}\n"
                                             f"Кофе по подписке: {db.get_coffee_today(client_id)}\n"
                                             f"Тип подписки: 30",
                                   reply_markup=keyboard)

            await callback.message.edit_text("Напишите комментарий к заказу одним сообщением и я передам его в кофейню")
            db.set_signup(client_id, "comment")

        else:   # Если клиент сегодня уже получил кофе
            next_coffee = int(db.get_time_update(1)) - int(time.time())
            await bot.send_message(client_id,
                                   f"Следующий кофе по подписке можно получить через: {str(datetime.timedelta(seconds=next_coffee))}")

    elif action == "substatus":     # Оставшееся время подписки
        if db.get_sub_status(client_id):
            await callback.message.edit_text(f"Подписка активна ✅\n"
                                             f"До конца подписки осталось: {time_sub_day(db.get_end_of_sub(client_id))}")
        else:
            await callback.message.edit_text("У вас нет подписки ❌", reply_markup=nav.get_inline_sub(client_id))

    elif action == "changenickname":        # Изменение имени
        await callback.message.edit_text("Введите новое имя")
        db.set_signup(client_id, "changenickname")

    elif action == "back":
        await callback.message.edit_text("☕️")

    else:
        await callback.message.edit_text("Ошибка при получении ответа")
    await callback.answer()


@dp.callback_query(F.data.startswith("sub_"))  # SUBSCRIPTION
async def sub(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    if action == "month":
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        if db.get_price(call.message.chat.id) == "3890":
            await bot.send_invoice(chat_id=call.message.chat.id,
                                   title="Оформление подписки",
                                   description="Подписка на 30 дней",
                                   payload="sub_month",
                                   provider_token=YOOTOKEN,
                                   currency="RUB",
                                   start_parameter="coffee_bot",
                                   prices=[types.LabeledPrice(label='Подписка на 30 дней', amount=3890 * 100)]
                                   )
        elif db.get_price(call.message.chat.id) == "3490":
            await bot.send_invoice(chat_id=call.message.chat.id,
                                   title="Оформление подписки",
                                   description="Подписка на 30 дней (Студенческая)",
                                   payload="sub_month",
                                   provider_token=YOOTOKEN,
                                   currency="RUB",
                                   start_parameter="coffee_bot",
                                   prices=[types.LabeledPrice(label='Подписка на 30 дней', amount=3490 * 100)]
                                   )


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
