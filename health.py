from aiohttp import web

async def home(request):
    return web.Response(text="Acki Wallet Bot Running!")

app = web.Application()
app.router.add_get("/", home)

def create_app():
    return app
