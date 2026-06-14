import os
import tempfile
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
import PyPDF2
from docx import Document

@Client.on_message(filters.document & filters.private)
async def handle_document(client, message: Message):
    doc = message.document
    file_name = doc.file_name
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext not in ['.pdf', '.docx', '.txt']:
        return
    
    processing_msg = await message.reply(f"📄 Processing `{file_name}`...")
    
    # Download file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file_name)
    await client.download_media(doc, file_name=file_path)
    
    try:
        text = ""
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages[:10]:  # Limit to 10 pages
                    text += page.extract_text()
        
        elif ext == '.docx':
            doc_obj = Document(file_path)
            text = '\n'.join([para.text for para in doc_obj.paragraphs[:200]])
        
        elif ext == '.txt':
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                text = await f.read()
                text = text[:5000]  # Limit to 5000 chars
        
        if text:
            # Use AI to summarize
            from ai_service.ai_provider import ai_provider
            summary = await ai_provider.generate_response(
                "gpt-3.5-turbo",
                [{"role": "user", "content": f"Summarize this document:\n\n{text}"}]
            )
            await processing_msg.edit(f"**📄 Document Summary:**\n\n{summary}")
        else:
            await processing_msg.edit("❌ Could not extract text from document.")
    
    except Exception as e:
        await processing_msg.edit(f"❌ Error: {str(e)}")
    
    finally:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
