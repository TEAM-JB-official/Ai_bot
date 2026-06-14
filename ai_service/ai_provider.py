import openai
import google.generativeai as genai
from config import config

class AIProvider:
    def __init__(self):
        self.openai_client = None
        self.deepseek_client = None
        self.gemini_model = None
        
        if "openai" in config.AI_API_KEYS:
            self.openai_client = openai.AsyncOpenAI(api_key=config.AI_API_KEYS["openai"])
        
        if "deepseek" in config.AI_API_KEYS:
            self.deepseek_client = openai.AsyncOpenAI(
                api_key=config.AI_API_KEYS["deepseek"],
                base_url="https://api.deepseek.com/v1"
            )
        
        if "gemini" in config.AI_API_KEYS:
            genai.configure(api_key=config.AI_API_KEYS["gemini"])
            self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    async def generate_response(self, model, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        provider = config.SUPPORTED_MODELS.get(model)
        
        if provider == "openai":
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif provider == "deepseek":
            response = await self.deepseek_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif provider == "gemini":
            # Convert messages format
            prompt = ""
            for msg in messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
            
            response = await self.gemini_model.generate_content_async(prompt)
            return response.text
        
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    async def analyze_code(self, code, language, task):
        """Analyze code for bugs, review, optimization"""
        prompts = {
            "debug": f"Find and fix bugs in this {language} code:\n\n{code}",
            "review": f"Review this {language} code for best practices, security, and performance:\n\n{code}",
            "optimize": f"Optimize this {language} code for better performance:\n\n{code}",
            "explain": f"Explain this {language} code line by line:\n\n{code}"
        }
        
        messages = [{"role": "user", "content": prompts.get(task, prompts["review"])}]
        return await self.generate_response("gpt-3.5-turbo", messages)
    
    async def generate_code(self, description, language):
        messages = [{"role": "user", "content": f"Generate {language} code for: {description}"}]
        return await self.generate_response("gpt-3.5-turbo", messages)
    
    async def generate_readme(self, project_info):
        messages = [{"role": "user", "content": f"Generate a professional README.md for this project:\n{project_info}"}]
        return await self.generate_response("gpt-3.5-turbo", messages)
    
    async def analyze_file(self, content, file_type):
        messages = [{"role": "user", "content": f"Analyze this {file_type} file:\n\n{content}"}]
        return await self.generate_response("gpt-3.5-turbo", messages)

ai_provider = AIProvider()
