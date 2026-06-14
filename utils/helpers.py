from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👥 Referral", callback_data="referral"),
            InlineKeyboardButton("⭐ Premium", callback_data="premium_info")
        ]
    ])

def get_user_level(user_id):
    # Placeholder for user level determination
    return "user"
