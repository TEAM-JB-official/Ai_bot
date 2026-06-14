from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.mongodb import db
from config import config  # missing import added

async def help_command(client, message):
    help_text = """
**📚 Commands List**

**General Commands:**
/start - Start the bot
/help - Show this help message
/settings - Configure bot settings
/profile - View your profile
/model - Change AI model
/history - View conversation history
/clear - Clear chat history

**AI Features:**
Send any message to chat with AI
Reply to AI message with "regenerate" to retry
Reply with "continue" to extend response

**File Analysis:**
Send .py, .js, .html, .css, .json, .txt files
Send .zip for project analysis
Send .pdf, .docx for document analysis

**Coding Commands:**
/debug <code> - Debug code
/explain <code> - Explain code
/optimize <code> - Optimize code
/sql <query description> - Generate SQL
/regex <pattern description> - Generate regex
/dockerfile <requirements> - Generate Dockerfile

**Admin Commands (Owner only):**
/admin - Admin panel
/broadcast - Send broadcast message
/stats - Bot statistics
/premium <user_id> <days> - Add premium
/ban <user_id> - Ban user
/unban <user_id> - Unban user
/coupon <code> <days> - Create coupon
"""
    await message.reply(help_text)

async def profile_command(client, message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    is_premium = await db.is_premium(user_id)
    
    usage = user.get("daily_usage", 0)
    limit = config.PREMIUM_DAILY_LIMIT if is_premium else config.DAILY_FREE_LIMIT
    remaining = limit - usage
    
    text = f"""
**👤 User Profile**

🆔 ID: `{user_id}`
👑 Premium: {'✅ Yes' if is_premium else '❌ No'}
📊 Daily Usage: {usage}/{limit}
⏳ Remaining: {remaining}
👥 Referrals: {user.get('referral_count', 0)}
📅 Joined: {user.get('joined_date', 'Unknown')}
"""
    await message.reply(text)
