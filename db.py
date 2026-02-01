import sqlite3
import time


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_tg_name(self, user_id, tg_name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `tg_name` = ? WHERE `user_id` = ?", (tg_name, user_id,))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    def set_end_of_sub(self, user_id, end_of_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `end_of_sub` = ? WHERE `user_id` = ?", (end_of_sub, user_id,))

    def set_coffee_today(self, user_id, coffee_today):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `coffee_today` = ? WHERE `user_id` = ?", (coffee_today, user_id,))

    def set_type_sub(self, user_id, type_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `type_sub` = ? WHERE `user_id` = ?", (type_sub, user_id,))

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def set_comment(self, user_id, comment):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `comment` = ? WHERE `user_id` = ?", (comment, user_id,))

    def set_price_tg_name(self, tg_name, price):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `price` = ? WHERE `tg_name` = ?", (price, tg_name,))

    def set_telegram_payment_charge_id(self, user_id, telegram_payment_charge_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `telegram_payment_charge_id` = ? WHERE `user_id` = ?", (telegram_payment_charge_id, user_id,))

    def set_provider_payment_charge_id(self, user_id, provider_payment_charge_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `provider_payment_charge_id` = ? WHERE `user_id` = ?", (provider_payment_charge_id, user_id,))

    def get_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                id = str(row[0])
            return id

    def get_user_id_for_order(self, user_id):  # NO DELITE
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                user_id = str(row[0])
            return user_id

    def get_user_id(self, tg_name):
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `tg_name` = ?", (tg_name,)).fetchall()
            for row in result:
                user_id = str(row[0])
            return user_id

    def get_tg_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `tg_name` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                tg_name = str(row[0])
            return tg_name

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = str(row[0][:10])
            return time_sub

    def get_end_of_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `end_of_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                end_of_sub = int(row[0])
            return end_of_sub

    def get_type_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `type_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                type_sub = str(row[0])
            return type_sub

    def get_coffee_today(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `coffee_today` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                coffee_today = str(row[0])
            return coffee_today

    def get_action(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_comment(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `comment` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                comment = str(row[0])
            return comment

    def get_price(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `price` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                price = str(row[0])
            return price

    def get_price_tg_name(self, tg_name):
        with self.connection:
            result = self.cursor.execute("SELECT `price` FROM `users` WHERE `tg_name` = ?", (tg_name,)).fetchall()
            for row in result:
                price = str(row[0])
            return price

    def get_telegram_payment_charge_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `telegram_payment_charge_id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                telegram_payment_charge_id = str(row[0])
            return telegram_payment_charge_id

    def get_provider_payment_charge_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `provider_payment_charge_id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                provider_payment_charge_id = str(row[0])
            return provider_payment_charge_id

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `end_of_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()

    def get_users_tg_name(self):
        with self.connection:
            return self.cursor.execute("SELECT `tg_name` FROM `users`").fetchall()

    def change_status_coffee_today(self):
        with self.connection:
            return self.cursor.execute("SELECT `coffee_today` FROM `users`").fetchall()

    def get_sticker(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `sticker` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                sticker = str(row[0])
            return sticker

    def set_sticker(self, id, sticker):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `sticker` = ? WHERE `id` = ?", (sticker, id,))

    def get_status(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `status` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                status = str(row[0])
            return status

    def set_status(self, id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `status` = ? WHERE `id` = ?", (status, id,))

    def get_text(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `text` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                text = str(row[0])
            return text

    def set_text(self, id, text):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `text` = ? WHERE `id` = ?", (text, id,))

    def get_time_update(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_update` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                time_update = str(row[0])
            return time_update

    def set_time_update(self, id, time_update):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `time_update` = ? WHERE `id` = ?", (time_update, id,))

    def get_time_update_status(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_update` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                time_update = int(row[0])

            if time_update < int(time.time()):
                return True
            else:
                return False

    def set_student(self, id, student):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `student` = ? WHERE `id` = ?", (student, id,))

    def get_student(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `student` FROM `admin` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                student = str(row[0])
            return student
