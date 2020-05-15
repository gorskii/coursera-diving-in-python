import asyncio


async def handle_echo(reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter):
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    chars_to_strip = '\n'
    print(f"received {message.rstrip(chars_to_strip)} from {addr}")
    writer.close()


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
