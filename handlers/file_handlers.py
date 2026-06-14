import os
import zipfile
import tempfile
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from ai_service.ai_provider import ai_provider

SUPPORTED_EXTENSIONS = {'.py', '.js', '.html', '.css', '.json', '.txt'}

@Client.on_message(filters.document)
async def handle_file(client, message: Message):
    document = message.document
    file_name = document.file_name
    ext = os.path.splitext(file_name)[1].lower()
    
    processing_msg = await message.reply(f"📁 Analyzing `{file_name}`...")
    
    # Download file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file_name)
    
    async with aiofiles.open(file_path, 'wb') as f:
        await client.download_media(document, file_name=f.name)
    
    try:
        if ext in SUPPORTED_EXTENSIONS:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            analysis = await ai_provider.analyze_file(content, ext[1:])
            await processing_msg.edit(f"**Analysis of {file_name}:**\n\n{analysis}")
        
        elif ext == '.zip':
            # Analyze ZIP project
            project_files = []
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist[:20]:  # Limit to 20 files
                    project_files.append(file_info.filename)
            
            project_info = f"Project: {file_name}\nFiles: {', '.join(project_files)}"
            readme = await ai_provider.generate_readme(project_info)
            await processing_msg.edit(f"**📦 Project Analysis:**\n\n{readme}")
        
        else:
            await processing_msg.edit(f"⚠️ Unsupported file type: {ext}")
    
    except Exception as e:
        await processing_msg.edit(f"❌ Error analyzing file: {str(e)}")
    
    finally:
        # Cleanup
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
