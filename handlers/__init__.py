from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters

from .start import start_command
from .commands import help_command, profile_command
from .ai_chat import ai_chat, handle_ai_callbacks
from .file_handlers import handle_file
from .document_handlers import handle_document
from .admin import admin_panel, broadcast_command, add_premium
from .callback import handle_callbacks
from .settings import settings_command, settings_callbacks

async def register_handlers(app):
    """Register all handlers with the Pyrogram app instance using proper wrappers"""
    
    # Command handlers
    app.add_handler(MessageHandler(start_command, filters.command("start")))
    app.add_handler(MessageHandler(help_command, filters.command("help")))
    app.add_handler(MessageHandler(profile_command, filters.command("profile")))
    app.add_handler(MessageHandler(settings_command, filters.command("settings")))
    app.add_handler(MessageHandler(admin_panel, filters.command("admin")))
    app.add_handler(MessageHandler(broadcast_command, filters.command("broadcast")))
    app.add_handler(MessageHandler(add_premium, filters.command("premium")))
    
    # File and document handlers
    app.add_handler(MessageHandler(handle_file, filters.document))
    app.add_handler(MessageHandler(handle_document, filters.document))
    
    # Text message handler (catches all private non-command messages)
    app.add_handler(MessageHandler(ai_chat, filters.text & ~filters.command([]) & filters.private))
    
    # Callback query handlers
    app.add_handler(CallbackQueryHandler(handle_callbacks))
    app.add_handler(CallbackQueryHandler(handle_ai_callbacks))
    app.add_handler(CallbackQueryHandler(settings_callbacks))

__all__ = ["register_handlers"]
