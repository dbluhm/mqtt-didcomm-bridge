from aries_staticagent import StaticConnection, crypto
from aiohttp import web

class PrintDispatcher:
    async def dispatch(self, msg, *args, **kwargs):
        print('Got:', msg.pretty_print())

def main():
    conn = StaticConnection(crypto.create_keypair(), dispatcher=PrintDispatcher())
    print('Verkey:', conn.verkey_b58)
    async def handle(request):
        """aiohttp handle POST."""
        response = []
        with conn.reply_handler(response.append):
            await conn.handle(await request.read())

        if response:
            return web.Response(text=response.pop())

        raise web.HTTPAccepted()

    app = web.Application()
    app.add_routes([web.post('/', handle)])

    web.run_app(app, port=3000)

if __name__ == '__main__':
    main()
