# ==============================
# SOURCE LIGHT — BOT
# ==============================

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from config import (
    BOT_TOKEN,
    OWNER_ID,
    EMOJI_SOURCE,
    EMOJI_CHECK,
    EMOJI_PROFILE,
    EMOJI_ID,
    EMOJI_USERNAME,
    EMOJI_UNKNOWN,
    EMOJI_SCAM,
    EMOJI_GARANT,
    EMOJI_ADMIN,
    EMOJI_OWNER,
    premium_emoji,
)

from database import (
    init_db,
    add_or_update_user,
    get_user_by_id,
    get_user_by_username,
    set_role,
)


# ==============================
# LOGGING
# ==============================

logging.basicConfig(level=logging.INFO)


# ==============================
# BOT
# ==============================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML"
    )
)

dp = Dispatcher()


# ==============================
# PREMIUM CUSTOM EMOJI
# ==============================

SOURCE = premium_emoji(
    EMOJI_SOURCE,
    "✨"
)

CHECK = premium_emoji(
    EMOJI_CHECK,
    "🔎"
)

PROFILE = premium_emoji(
    EMOJI_PROFILE,
    "👤"
)

ID_ICON = premium_emoji(
    EMOJI_ID,
    "🆔"
)

USERNAME = premium_emoji(
    EMOJI_USERNAME,
    "🔗"
)

UNKNOWN = premium_emoji(
    EMOJI_UNKNOWN,
    "❔"
)

SCAM = premium_emoji(
    EMOJI_SCAM,
    "⛔"
)

GARANT = premium_emoji(
    EMOJI_GARANT,
    "💎"
)

ADMIN = premium_emoji(
    EMOJI_ADMIN,
    "🛡"
)

OWNER = premium_emoji(
    EMOJI_OWNER,
    "👑"
)


# ==============================
# ROLE NAMES
# ==============================

ROLE_NAMES = {
    "user": "Пользователь",
    "scam": f"{SCAM} SCAM",
    "garant": f"{GARANT} Гарант",
    "admin": f"{ADMIN} Администратор",
    "owner": f"{OWNER} Владелец",
}


# ==============================
# REGISTER USER
# ==============================

async def register_message_user(message: Message):

    if not message.from_user:
        return

    add_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )


# ==============================
# FORMAT PROFILE
# ==============================

def format_user(user):

    telegram_id, username, first_name, role = user

    name = first_name or "Не указано"

    if username:
        username_text = f"@{username}"
    else:
        username_text = "Не указан"

    role_text = ROLE_NAMES.get(
        role,
        "Пользователь"
    )

    return (
        f"{PROFILE} <b>ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"{PROFILE} <b>Имя</b>\n"
        f"└ {name}\n\n"

        f"{USERNAME} <b>Username</b>\n"
        f"└ {username_text}\n\n"

        f"{ID_ICON} <b>Telegram ID</b>\n"
        f"└ <code>{telegram_id}</code>\n\n"

        f"{SOURCE} <b>Статус</b>\n"
        f"└ {role_text}\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"{SOURCE} "
        f"<i>Информация предоставлена системой Source Light.</i>"
    )


# ==============================
# /START
# ==============================

@dp.message(Command("start"))
async def start_handler(message: Message):

    await register_message_user(message)

    text = (
        f"{SOURCE} <b>SOURCE LIGHT</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"Добро пожаловать в систему "
        f"проверки пользователей Telegram.\n\n"

        f"{CHECK} <b>Проверка пользователя</b>\n"
        f"Ответь на сообщение пользователя командой "
        f"<code>/check</code>.\n\n"

        f"{PROFILE} <b>Личный профиль</b>\n"
        f"Используй <code>/me</code>, чтобы посмотреть "
        f"информацию о своём аккаунте.\n\n"

        f"{SOURCE} "
        f"<i>Source Light — база доверия пользователей.</i>"
    )

    await message.answer(text)


# ==============================
# /ME
# ==============================

@dp.message(Command("me"))
async def me_handler(message: Message):

    await register_message_user(message)

    user = get_user_by_id(
        message.from_user.id
    )

    if not user:

        await message.answer(
            f"{UNKNOWN} <b>ПРОФИЛЬ НЕ НАЙДЕН</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"Попробуй отправить команду ещё раз."
        )

        return

    await message.answer(
        format_user(user)
    )


# ==============================
# FIND USER
# ==============================

def find_check_user(message: Message):

    # /check @username

    if message.text:

        parts = message.text.split(
            maxsplit=1
        )

        if len(parts) == 2:

            target = parts[1].strip()

            if target.startswith("@"):

                return get_user_by_username(
                    target
                )

    # /check reply

    if message.reply_to_message:

        target_message = (
            message.reply_to_message
        )

        if not target_message.from_user:
            return None

        target_id = (
            target_message.from_user.id
        )

        return get_user_by_id(
            target_id
        )

    return None


# ==============================
# /CHECK
# ==============================

@dp.message(Command("check"))
async def check_handler(message: Message):

    await register_message_user(message)

    user = find_check_user(message)

    if user:

        await message.answer(
            f"{CHECK} <b>РЕЗУЛЬТАТ ПРОВЕРКИ</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"{format_user(user)}"
        )

        return

    # Проверка через reply

    if message.reply_to_message:

        target = (
            message.reply_to_message.from_user
        )

        if target:

            username_text = (
                f"@{target.username}"
                if target.username
                else "Не указан"
            )

            await message.answer(
                f"{UNKNOWN} "
                f"<b>НЕИЗВЕСТНЫЙ ПОЛЬЗОВАТЕЛЬ</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"

                f"{PROFILE} <b>Имя</b>\n"
                f"└ {target.first_name or 'Не указано'}\n\n"

                f"{USERNAME} <b>Username</b>\n"
                f"└ {username_text}\n\n"

                f"{ID_ICON} <b>Telegram ID</b>\n"
                f"└ <code>{target.id}</code>\n\n"

                f"{UNKNOWN} <b>Статус</b>\n"
                f"└ Неизвестен\n\n"

                f"━━━━━━━━━━━━━━━━━━\n"
                f"{SOURCE} "
                f"<i>Пользователь отсутствует "
                f"в базе Source Light.</i>"
            )

            return

    # /check @username

    if message.text:

        parts = message.text.split(
            maxsplit=1
        )

        if len(parts) == 2:

            target = parts[1].strip()

            if target.startswith("@"):

                await message.answer(
                    f"{UNKNOWN} "
                    f"<b>ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН</b>\n"
                    f"━━━━━━━━━━━━━━━━━━\n\n"

                    f"Пользователь "
                    f"<b>{target}</b> "
                    f"отсутствует в базе.\n\n"

                    f"{SOURCE} "
                    f"<i>Пользователь должен быть "
                    f"известен системе.</i>"
                )

                return

    await message.answer(
        f"{CHECK} <b>КАК ПРОВЕРИТЬ</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"Ответь на сообщение пользователя:\n"
        f"<code>/check</code>\n\n"

        f"Или используй:\n"
        f"<code>/check @username</code>\n\n"

        f"{SOURCE} "
        f"<i>Source Light покажет "
        f"сохранённый статус пользователя.</i>"
    )


# ==============================
# OWNER CHECK
# ==============================

def is_owner(message: Message) -> bool:

    return (
        message.from_user is not None
        and message.from_user.id == OWNER_ID
    )


# ==============================
# GET USERNAME FROM COMMAND
# ==============================

def get_username_argument(
    message: Message
):

    if not message.text:
        return None

    parts = message.text.strip().split(
        maxsplit=1
    )

    if len(parts) != 2:
        return None

    username = parts[1].strip()

    if not username.startswith("@"):
        return None

    return username


# ==============================
# +SCAM @USERNAME
# ==============================

@dp.message(
    F.text.regexp(
        r"^\+scam\s+@\w+$"
    )
)
async def scam_handler(message: Message):

    if not is_owner(message):
        return

    username = get_username_argument(
        message
    )

    if not username:

        await message.answer(
            f"{SCAM} <b>НЕВЕРНЫЙ ФОРМАТ</b>\n\n"
            f"Используй:\n"
            f"<code>+scam @username</code>"
        )

        return

    user = get_user_by_username(
        username
    )

    if not user:

        await message.answer(
            f"{UNKNOWN} "
            f"<b>ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"

            f"Пользователь "
            f"<b>{username}</b> "
            f"отсутствует в базе Source Light."
        )

        return

    user_id = user[0]

    set_role(
        user_id,
        "scam"
    )

    await message.answer(
        f"{SCAM} <b>СТАТУС ИЗМЕНЁН</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"{PROFILE} <b>Пользователь:</b>\n"
        f"└ {username}\n\n"

        f"{ID_ICON} <b>Telegram ID:</b>\n"
        f"└ <code>{user_id}</code>\n\n"

        f"{SCAM} <b>Новый статус:</b>\n"
        f"└ SCAM\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"{SOURCE} Запись сохранена в базе."
    )


# ==============================
# +GARANT @USERNAME
# +GUARANTEE @USERNAME
# ==============================

@dp.message(
    F.text.regexp(
        r"^\+(garant|guarantee)\s+@\w+$"
    )
)
async def garant_handler(message: Message):

    if not is_owner(message):
        return

    username = get_username_argument(
        message
    )

    if not username:

        await message.answer(
            f"{GARANT} <b>НЕВЕРНЫЙ ФОРМАТ</b>\n\n"
            f"Используй:\n"
            f"<code>+garant @username</code>"
        )

        return

    user = get_user_by_username(
        username
    )

    if not user:

        await message.answer(
            f"{UNKNOWN} "
            f"<b>ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"

            f"Пользователь "
            f"<b>{username}</b> "
            f"отсутствует в базе Source Light."
        )

        return

    user_id = user[0]

    set_role(
        user_id,
        "garant"
    )

    await message.answer(
        f"{GARANT} <b>СТАТУС ИЗМЕНЁН</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"{PROFILE} <b>Пользователь:</b>\n"
        f"└ {username}\n\n"

        f"{ID_ICON} <b>Telegram ID:</b>\n"
        f"└ <code>{user_id}</code>\n\n"

        f"{GARANT} <b>Новый статус:</b>\n"
        f"└ Гарант\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"{SOURCE} Запись сохранена в базе."
    )


# ==============================
# +ADMIN @USERNAME
# ==============================

@dp.message(
    F.text.regexp(
        r"^\+admin\s+@\w+$"
    )
)
async def admin_handler(message: Message):

    if not is_owner(message):
        return

    username = get_username_argument(
        message
    )

    if not username:

        await message.answer(
            f"{ADMIN} <b>НЕВЕРНЫЙ ФОРМАТ</b>\n\n"
            f"Используй:\n"
            f"<code>+admin @username</code>"
        )

        return

    user = get_user_by_username(
        username
    )

    if not user:

        await message.answer(
            f"{UNKNOWN} "
            f"<b>ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"

            f"Пользователь "
            f"<b>{username}</b> "
            f"отсутствует в базе Source Light."
        )

        return

    user_id = user[0]

    set_role(
        user_id,
        "admin"
    )

    await message.answer(
        f"{ADMIN} <b>СТАТУС ИЗМЕНЁН</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"

        f"{PROFILE} <b>Пользователь:</b>\n"
        f"└ {username}\n\n"

        f"{ID_ICON} <b>Telegram ID:</b>\n"
        f"└ <code>{user_id}</code>\n\n"

        f"{ADMIN} <b>Новый статус:</b>\n"
        f"└ Администратор\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"
        f"{SOURCE} Запись сохранена в базе."
    )


# ==============================
# START BOT
# ==============================

async def main():

    init_db()

    print("Source Light запущен.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
