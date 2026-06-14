from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    joined_date: datetime = Field(default_factory=datetime.utcnow)
    is_banned: bool = False
    daily_usage: int = 0
    last_reset: datetime = Field(default_factory=datetime.utcnow)
    referral_count: int = 0
    referred_by: Optional[int] = None
    model: Optional[str] = None  # User's selected AI model

class Premium(BaseModel):
    user_id: int
    expires_at: datetime
    plan: str = "monthly"  # monthly, yearly, lifetime
    activated_at: datetime = Field(default_factory=datetime.utcnow)

class Referral(BaseModel):
    user_id: int
    referred_users: List[int] = []
    total_earned: int = 0
    claimed: bool = False

class Conversation(BaseModel):
    user_id: int
    chat_id: int
    messages: List[Dict[str, str]] = []  # [{"role": "user/assistant", "content": "..."}]
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Coupon(BaseModel):
    code: str
    days: int
    max_uses: int = 1
    used_count: int = 0
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

class Stat(BaseModel):
    user_id: int
    ai_calls: int = 0
    file_analyses: int = 0
    doc_analyses: int = 0
    code_generations: int = 0
    total_tokens_used: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class AdminLog(BaseModel):
    admin_id: int
    action: str
    target_user_id: Optional[int] = None
    details: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
