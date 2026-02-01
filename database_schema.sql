-- Структура базы данных для Subscription Coffee Bot

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL UNIQUE,
    "tg_name" TEXT,
    "nickname" TEXT,
    "time_sub" TEXT NOT NULL DEFAULT '0',
    "end_of_sub" TEXT NOT NULL DEFAULT '0',
    "type_sub" TEXT NOT NULL DEFAULT '0',
    "coffee_today" TEXT NOT NULL DEFAULT '0',
    "signup" TEXT DEFAULT 'setnickname',
    "comment" TEXT DEFAULT '0',
    "price" INTEGER DEFAULT 3890,
    "telegram_payment_charge_id" TEXT,
    "provider_payment_charge_id" TEXT
);

-- Таблица администраторов
CREATE TABLE IF NOT EXISTS "admin" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tg_id" INTEGER,
    "sticker" TEXT,
    "text" TEXT,
    "status" TEXT DEFAULT 'done',
    "time_update" INTEGER,
    "student" TEXT
);

-- Индексы для ускорения запросов
CREATE INDEX IF NOT EXISTS "idx_users_user_id" ON "users" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_users_tg_name" ON "users" ("tg_name");
CREATE INDEX IF NOT EXISTS "idx_users_end_of_sub" ON "users" ("end_of_sub");

-- Вставка начальных данных для админ-панели
INSERT OR IGNORE INTO "admin" ("id", "time_update") VALUES (1, strftime('%s', 'now'));

-- Комментарии к таблицам
COMMENT ON TABLE "users" IS 'Таблица пользователей бота';
COMMENT ON TABLE "admin" IS 'Таблица для настроек админ-панели';