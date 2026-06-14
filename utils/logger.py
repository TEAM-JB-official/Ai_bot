import logging
from config import config
from pyrogram import Client

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

async def log_to_channel(client, text):
    if config.LOG_CHANNEL_ID:
        try:
            await client.send_message(config.LOG_CHANNEL_ID, text)
        except:
            pass
