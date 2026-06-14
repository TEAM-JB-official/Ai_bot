# utils/premium.py
from database.mongodb import db
from datetime import datetime

async def check_premium_status(user_id: int) -> dict:
    """Check user's premium status and return details"""
    is_premium = await db.is_premium(user_id)
    premium_data = await db.premium.find_one({"user_id": user_id})
    
    if is_premium and premium_data:
        expires_at = premium_data.get("expires_at")
        days_left = (expires_at - datetime.utcnow()).days if expires_at else 0
        return {
            "is_premium": True,
            "plan": premium_data.get("plan", "monthly"),
            "expires_at": expires_at,
            "days_left": days_left
        }
    else:
        return {
            "is_premium": False,
            "plan": None,
            "expires_at": None,
            "days_left": 0
        }
