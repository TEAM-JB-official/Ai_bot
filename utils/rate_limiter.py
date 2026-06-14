from database.mongodb import db
from config import config
from datetime import datetime, timedelta

async def check_rate_limit(user_id):
    user = await db.get_user(user_id)
    if not user:
        return True
    
    # Reset daily usage if new day
    last_reset = user.get("last_reset")
    if last_reset and (datetime.utcnow() - last_reset) > timedelta(days=1):
        await db.reset_daily_usage()
        user = await db.get_user(user_id)
    
    is_premium = await db.is_premium(user_id)
    limit = config.PREMIUM_DAILY_LIMIT if is_premium else config.DAILY_FREE_LIMIT
    usage = user.get("daily_usage", 0)
    
    return usage < limit
