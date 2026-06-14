from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.mongodb import db
from utils.helpers import create_start_keyboard

async def start_command(client, message):
    user_id = message.from_user.id
    args = message.text.split()
    
    # Handle referral
    referred_by = None
    if len(args) > 1 and args[1].startswith("ref_"):
        referred_by = int(args[1].split("_")[1])
    
    # Get or create user
    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id, message.from_user.username, 
                            message.from_user.first_name, referred_by)
        if referred_by:
            await db.users.update_one(
                {"user_id": referred_by},
                {"$inc": {"referral_count": 1}}
            )
    
    # Check if banned
    if user and user.get("is_banned", False):
        await message.reply("🚫 You are banned from using this bot.")
        return
    
    # Welcome message
    welcome_text = f"""
**🤖 Welcome to AI Coding Assistant Bot!**

Your ultimate coding companion powered by multiple AI models.

**✨ Features:**
• 💬 AI Chat with memory
• 💻 Code generation & debugging
• 📁 File analysis (Python, JS, HTML, JSON, ZIP)
• 📄 Document analysis (PDF, DOCX, TXT)
• 🔧 SQL & Regex generator
• 🐳 Dockerfile generator
• 👥 Referral system
• ⭐ Premium features

**🚀 Quick Commands:**
/help - Show all commands
/model - Change AI model
/settings - Bot settings
/history - View conversation history
/clear - Clear chat history

Use me in groups or PM me directly!
    """
    
    keyboard = create_start_keyboard()
    await message.reply(welcome_text, reply_markup=keyboard)
