from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import config
from database.mongodb import db
from datetime import datetime, timedelta
import asyncio

def owner_only(func):
    async def wrapper(client, message):
        if message.from_user.id != config.OWNER_ID:
            await message.reply("⛔ Owner only command!")
            return
        return await func(client, message)
    return wrapper

@owner_only
async def admin_panel(client, message):
    total_users = await db.users.count_documents({})
    premium_users = await db.premium.count_documents({"expires_at": {"$gt": datetime.utcnow()}})
    banned_users = await db.users.count_documents({"is_banned": True})
    
    text = f"""
**👑 Admin Panel**

📊 **Statistics:**
Total Users: {total_users}
Premium Users: {premium_users}
Banned Users: {banned_users}

📈 **Today's Usage:**
...
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("👥 User List", callback_data="admin_users")],
        [InlineKeyboardButton("⭐ Manage Premium", callback_data="admin_premium")],
        [InlineKeyboardButton("🎫 Coupons", callback_data="admin_coupons")]
    ])
    
    await message.reply(text, reply_markup=keyboard)

@owner_only
async def broadcast_command(client, message):
    # Simple implementation - in production, add confirmation and async sending
    text = message.text.split("/broadcast", 1)[1].strip()
    if not text:
        await message.reply("Usage: /broadcast <message>")
        return
    
    count = 0
    async for user in db.users.find({}):
        try:
            await client.send_message(user["user_id"], text)
            count += 1
            await asyncio.sleep(0.05)  # Rate limit
        except:
            pass
    
    await message.reply(f"✅ Broadcast sent to {count} users")

@owner_only
async def add_premium(client, message):
    parts = message.text.split()
    if len(parts) != 3:
        await message.reply("Usage: /premium <user_id> <days>")
        return
    
    user_id = int(parts[1])
    days = int(parts[2])
    
    await db.add_premium(user_id, days)
    await message.reply(f"✅ Added {days} days premium to user {user_id}")
    
    # Notify user
    try:
        await client.send_message(user_id, f"🎉 You've been granted {days} days of premium access!")
    except:
        pass
