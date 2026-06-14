from .start import start_command
from .commands import help_command, profile_command
from .ai_chat import ai_chat, handle_ai_callbacks
from .file_handlers import handle_file
from .document_handlers import handle_document
from .admin import admin_panel, broadcast_command, add_premium
from .callback import handle_callbacks
from .settings import settings_command, settings_callbacks

async def register_handlers(app):
    """Register all handlers with the Pyrogram app instance"""
    
    # Command handlers
    app.add_handler(start_command)
    app.add_handler(help_command)
    app.add_handler(profile_command)
    app.add_handler(settings_command)
    app.add_handler(admin_panel)
    app.add_handler(broadcast_command)
    app.add_handler(add_premium)
    
    # Message handlers (order matters: specific before generic)
    app.add_handler(handle_file)       # documents
    app.add_handler(handle_document)   # pdf, docx, txt
    app.add_handler(ai_chat)           # text messages – must be last
    
    # Callback query handlers
    app.add_handler(handle_callbacks)
    app.add_handler(handle_ai_callbacks)
    app.add_handler(settings_callbacks)

__all__ = [
    "register_handlers"
]
