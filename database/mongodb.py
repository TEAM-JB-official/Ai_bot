from motor.motor_asyncio import AsyncIOMotorClient
from config import config

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.premium = None
        self.referrals = None
        self.conversations = None
        self.coupons = None
        self.stats = None
    
    async def connect(self):
        self.client = AsyncIOMotorClient(config.MONGO_URI)
        self.db = self.client[config.MONGO_DB_NAME]
        self.users = self.db.users
        self.premium = self.db.premium
        self.referrals = self.db.referrals
        self.conversations = self.db.conversations
        self.coupons = self.db.coupons
        self.stats = self.db.stats
        
        # Create indexes
        await self.users.create_index("user_id", unique=True)
        await self.premium.create_index("user_id", unique=True)
        await self.referrals.create_index("user_id", unique=True)
        await self.conversations.create_index([("user_id", 1), ("chat_id", 1)])
        await self.coupons.create_index("code", unique=True)
    
    async def get_user(self, user_id):
        return await self.users.find_one({"user_id": user_id})
    
    async def create_user(self, user_id, username=None, first_name=None, referred_by=None):
        user = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "joined_date": datetime.utcnow(),
            "is_banned": False,
            "daily_usage": 0,
            "last_reset": datetime.utcnow(),
            "referral_count": 0,
            "referred_by": referred_by
        }
        await self.users.insert_one(user)
        return user
    
    async def update_user_usage(self, user_id, increment=1):
        await self.users.update_one(
            {"user_id": user_id},
            {"$inc": {"daily_usage": increment}}
        )
    
    async def reset_daily_usage(self):
        await self.users.update_many(
            {},
            {"$set": {"daily_usage": 0, "last_reset": datetime.utcnow()}}
        )
    
    async def is_premium(self, user_id):
        premium = await self.premium.find_one({"user_id": user_id})
        if premium and premium.get("expires_at", datetime.min) > datetime.utcnow():
            return True
        return False
    
    async def add_premium(self, user_id, days, plan="monthly"):
        expires_at = datetime.utcnow() + timedelta(days=days)
        await self.premium.update_one(
            {"user_id": user_id},
            {"$set": {"expires_at": expires_at, "plan": plan, "activated_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def save_conversation(self, user_id, chat_id, messages):
        await self.conversations.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"messages": messages[-20:], "updated_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def get_conversation(self, user_id, chat_id):
        conv = await self.conversations.find_one({"user_id": user_id, "chat_id": chat_id})
        return conv.get("messages", []) if conv else []
    
    async def clear_conversation(self, user_id, chat_id):
        await self.conversations.delete_one({"user_id": user_id, "chat_id": chat_id})
    
    async def get_user_stats(self, user_id):
        return await self.stats.find_one({"user_id": user_id})
    
    async def increment_stat(self, user_id, field):
        await self.stats.update_one(
            {"user_id": user_id},
            {"$inc": {field: 1}},
            upsert=True
        )

from datetime import datetime, timedelta
db = Database()
