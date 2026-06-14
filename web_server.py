from aiohttp import web
import asyncio
import threading

async def health_check(request):
    return web.Response(text="OK")

async def start_web_server(port=8080):
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server running on port {port}")

def run_web_server(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_web_server(port))
    loop.run_forever()
