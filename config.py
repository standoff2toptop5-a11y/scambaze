# ==============================
# SOURCE LIGHT — CONFIG
# ==============================

# ВАЖНО: сюда вставь НОВЫЙ токен после перевыпуска
BOT_TOKEN = "8959377856:AAHhW4iOoS9pnnoUPYHDf5wgYfKfo43YzFA"

# Telegram ID владельца
OWNER_ID = 914164018


# ==============================
# PREMIUM CUSTOM EMOJI
# ==============================

# SOURCE
EMOJI_SOURCE = "5188217332748527444"

# CHECK
EMOJI_CHECK = "5316924123786524990"

# PROFILE
EMOJI_PROFILE = "5778145208411624388"

# ID
EMOJI_ID = "5422683699130933153"

# USERNAME
EMOJI_USERNAME = "5447588260270341594"

# UNKNOWN
EMOJI_UNKNOWN = "5341330417179976367"

# SCAM
EMOJI_SCAM = "6217490044618281742"

# GARANT
EMOJI_GARANT = "6217739736837000786"

# ADMIN
EMOJI_ADMIN = "6269458311381258421"

# OWNER
EMOJI_OWNER = "5217822164362739968"


# ==============================
# PREMIUM EMOJI FUNCTION
# ==============================

def premium_emoji(emoji_id: str, fallback: str) -> str:
    """
    Возвращает Premium Custom Emoji.
    Если ID неправильный/пустой — использует обычный emoji.
    """

    if not emoji_id or emoji_id == "ВСТАВЬ_ID":
        return fallback

    # ID должен состоять только из цифр
    if not emoji_id.isdigit():
        return fallback

    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
