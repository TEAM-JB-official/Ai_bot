from .start import start_command
from .commands import help_command, profile_command
from .ai_chat import ai_chat, handle_ai_callbacks
from .file_handlers import handle_file
from .document_handlers import handle_document
from .admin import admin_panel, broadcast_command, add_premium
from .callback import handle_callbacks
from .settings import settings_command, settings_callbacks

async def register_handlers(app):
    """Register all handlers with the Pyrogram app"""
    # Handlers are automatically registered when modules are imported
    # This function is kept for compatibility with main.py
    pass

__all__ = [
    "start_command",
    "help_command",
    "profile_command",
    "ai_chat",
    "handle_ai_callbacks",
    "handle_file",
    "handle_document",
    "admin_panel",
    "broadcast_command",
    "add_premium",
    "handle_callbacks",
    "settings_command",
    "settings_callbacks",
    "register_handlers"
]
