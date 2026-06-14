from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongodb import db
from config import config

async def settings_command(client, message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    current_model = user.get("model", config.DEFAULT_MODEL)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🤖 Model: {current_model}", callback_data="change_model")],
        [InlineKeyboardButton("🗑️ Clear All Data", callback_data="delete_data")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
    ])
    
    await message.reply("⚙️ **Bot Settings**\nConfigure your preferences:", reply_markup=keyboard)

async def settings_callbacks(client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if data == "change_model":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("GPT-3.5 Turbo", callback_data="set_model_gpt-3.5-turbo")],
            [InlineKeyboardButton("GPT-4", callback_data="set_model_gpt-4")],
            [InlineKeyboardButton("DeepSeek Chat", callback_data="set_model_deepseek-chat")],
            [InlineKeyboardButton("Gemini Pro", callback_data="set_model_gemini-pro")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_back")]
        ])
        await callback_query.message.edit_text("Select AI model:", reply_markup=keyboard)
    
    elif data.startswith("set_model_"):
        model = data.replace("set_model_", "")
        await db.users.update_one({"user_id": user_id}, {"$set": {"model": model}})
        await callback_query.answer(f"✅ Model changed to {model}")
        await settings_command(client, callback_query.message)
    
    elif data == "settings_back":
        await settings_command(client, callback_query.message)
    
    await callback_query.answer()
