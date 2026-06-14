from pyrogram.types import CallbackQuery

async def handle_callbacks(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "help":
        from .commands import help_command
        await help_command(client, callback_query.message)
    
    elif data == "referral":
        user_id = callback_query.from_user.id
        referral_link = f"https://t.me/{(await client.get_me()).username}?start=ref_{user_id}"
        text = f"**👥 Referral System**\n\nShare your referral link and earn rewards!\n\nYour link:\n`{referral_link}`\n\nEach referral gives you bonus usage!"
        await callback_query.message.reply(text)
    
    elif data == "premium_info":
        text = """
⭐ **Premium Benefits:**
• 10x higher daily limit
• Access to GPT-4 and other advanced models
• Priority processing
• Longer conversation memory
• Advanced code analysis features

**Get Premium:**
Contact @admin to purchase premium or use coupon codes.
        """
        await callback_query.message.reply(text)
    
    elif data == "admin_broadcast":
        await callback_query.message.reply("Send the broadcast message (reply to this message):")
        # Store state for broadcast
        
    await callback_query.answer()
