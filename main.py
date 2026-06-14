import asyncio
from pyrogram import Client, idle
from pyrogram.enums import ParseMode
from config import config
from database.mongodb import db
from handlers import register_handlers
from utils.logger import setup_logger
from web_server import start_web_server

async def main():
    logger = setup_logger()
    
    await db.connect()
    logger.info("Connected to MongoDB")
    
    app = Client(
        "ai_coding_bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        parse_mode=ParseMode.MARKDOWN
    )
    
    await register_handlers(app)
    await app.start()
    logger.info(f"Bot started as @{(await app.get_me()).username}")
    
    # Start web server for health checks (Koyeb requirement)
    asyncio.create_task(start_web_server(config.PORT))
    logger.info(f"Web server started on port {config.PORT}")
    
    await idle()
    
    await app.stop()
    logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
