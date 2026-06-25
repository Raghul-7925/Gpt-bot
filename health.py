from aiohttp import web

async def health(request):
    return web.Response(text="OK")

def create_app():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    return app
