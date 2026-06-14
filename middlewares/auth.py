from typing import Callable, Dict, Any
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from database.mongodb import db
from config import config
from datetime import datetime, timedelta

class AuthMiddleware:
    """Middleware for authentication, rate limiting, and premium checks"""
    
    @staticmethod
    async def check_force_subscribe(client: Client, user_id: int) -> bool:
        """Check if user is subscribed to required channel"""
        if not config.FORCE_SUBSCRIBE_CHANNEL:
            return True
        
        try:
            member = await client.get_chat_member(config.FORCE_SUBSCRIBE_CHANNEL, user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
            else:
                await client.send_message(
                    user_id,
                    f"⚠️ Please join our [channel](https://t.me/{config.FORCE_SUBSCRIBE_CHANNEL}) to use this bot.",
                    disable_web_page_preview=True
                )
                return False
        except Exception:
            return False
    
    @staticmethod
    async def check_rate_limit(user_id: int) -> bool:
        """Check if user has exceeded daily limit"""
        user = await db.get_user(user_id)
        if not user:
            return True
        
        # Reset daily usage if new day
        last_reset = user.get("last_reset")
        if last_reset and (datetime.utcnow() - last_reset) > timedelta(days=1):
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"daily_usage": 0, "last_reset": datetime.utcnow()}}
            )
            user = await db.get_user(user_id)
        
        is_premium = await db.is_premium(user_id)
        limit = config.PREMIUM_DAILY_LIMIT if is_premium else config.DAILY_FREE_LIMIT
        usage = user.get("daily_usage", 0)
        
        if usage >= limit:
            return False
        return True
    
    @staticmethod
    async def increment_usage(user_id: int):
        """Increment user daily usage counter"""
        await db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"daily_usage": 1}}
        )
    
    @staticmethod
    async def is_user_banned(user_id: int) -> bool:
        """Check if user is banned"""
        user = await db.get_user(user_id)
        return user.get("is_banned", False) if user else False
    
    @staticmethod
    async def get_user_model(user_id: int) -> str:
        """Get user's preferred AI model"""
        user = await db.get_user(user_id)
        if user and user.get("model"):
            return user["model"]
        return config.DEFAULT_MODEL

    @staticmethod
    async def is_premium(user_id: int) -> bool:
        """Check if user has premium subscription"""
        return await db.is_premium(user_id)


# Convenience functions for direct use in handlers
async def check_auth(client: Client, user_id: int, check_rate: bool = True, check_ban: bool = True) -> Dict[str, Any]:
    """Comprehensive auth check returns dict with status and message"""
    auth = AuthMiddleware()
    
    # Check force subscribe
    if not await auth.check_force_subscribe(client, user_id):
        return {"ok": False, "reason": "force_subscribe"}
    
    # Check ban
    if check_ban and await auth.is_user_banned(user_id):
        return {"ok": False, "reason": "banned", "message": "🚫 You are banned from using this bot."}
    
    # Check rate limit
    if check_rate and not await auth.check_rate_limit(user_id):
        return {"ok": False, "reason": "rate_limit", "message": "⚠️ Daily limit reached! Upgrade to premium for unlimited access."}
    
    return {"ok": True}
