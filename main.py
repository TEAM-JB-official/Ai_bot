import asyncio
from pyrogram import Client, idle
from pyrogram.enums import ParseMode
from config import config
from database.mongodb import db
from handlers import register_handlers
from utils.logger import setup_logger

async def main():
    # Setup logger
    logger = setup_logger()
    
    # Connect to MongoDB
    await db.connect()
    logger.info("Connected to MongoDB")
    
    # Initialize bot
    app = Client(
        "ai_coding_bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Register all handlers
    await register_handlers(app)
    
    # Start bot
    await app.start()
    logger.info(f"Bot started as @{(await app.get_me()).username}")
    
    # Keep bot running
    await idle()
    
    # Cleanup
    await app.stop()
    logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
