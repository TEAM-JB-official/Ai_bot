from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.mongodb import db
from ai_service.ai_provider import ai_provider
from config import config
from utils.rate_limiter import check_rate_limit
from utils.force_subscribe import check_force_subscribe

@Client.on_message(filters.text & ~filters.command([]) & filters.private)
async def ai_chat(client, message):
    user_id = message.from_user.id
    
    # Check force subscribe
    if not await check_force_subscribe(client, user_id):
        return
    
    # Check rate limit
    if not await check_rate_limit(user_id):
        await message.reply("⚠️ Daily limit reached! Upgrade to premium for unlimited access.")
        return
    
    # Get user's selected model
    user = await db.get_user(user_id)
    model = user.get("model", config.DEFAULT_MODEL)
    
    # Get conversation history
    messages = await db.get_conversation(user_id, message.chat.id)
    
    # Add current message
    messages.append({"role": "user", "content": message.text})
    
    # Get AI response
    thinking_msg = await message.reply("🤔 *Thinking...*")
    
    try:
        response = await ai_provider.generate_response(model, messages)
        
        # Save conversation
        messages.append({"role": "assistant", "content": response})
        await db.save_conversation(user_id, message.chat.id, messages)
        
        # Update usage
        await db.update_user_usage(user_id)
        await db.increment_stat(user_id, "ai_calls")
        
        # Send response with action buttons
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Regenerate", callback_data=f"regenerate_{model}"),
                InlineKeyboardButton("⏩ Continue", callback_data="continue")
            ],
            [InlineKeyboardButton("🗑️ Clear History", callback_data="clear_history")]
        ])
        
        await thinking_msg.delete()
        await message.reply(response, reply_markup=keyboard)
        
    except Exception as e:
        await thinking_msg.edit(f"❌ Error: {str(e)}")

@Client.on_callback_query()
async def handle_ai_callbacks(client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message
    
    if data.startswith("regenerate_"):
        model = data.split("_")[1]
        # Get last user message and regenerate
        conv = await db.get_conversation(user_id, message.chat.id)
        if len(conv) >= 2:
            # Remove last assistant response
            conv.pop()
            response = await ai_provider.generate_response(model, conv)
            conv.append({"role": "assistant", "content": response})
            await db.save_conversation(user_id, message.chat.id, conv)
            await message.edit(response)
    
    elif data == "continue":
        conv = await db.get_conversation(user_id, message.chat.id)
        if conv:
            continue_prompt = "Continue your previous response, extend it naturally."
            conv.append({"role": "user", "content": continue_prompt})
            response = await ai_provider.generate_response(model, conv)
            conv.append({"role": "assistant", "content": response})
            await db.save_conversation(user_id, message.chat.id, conv)
            await message.reply(response)
    
    elif data == "clear_history":
        await db.clear_conversation(user_id, message.chat.id)
        await callback_query.answer("✅ History cleared!")
    
    await callback_query.answer()
