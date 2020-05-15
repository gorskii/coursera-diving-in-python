import asyncio


async def handle_echo(reader, writer):
    pass


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001, loop=loop)
server = loop.run_until_complete(coro)  # type: asyncio.AbstractServer
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
