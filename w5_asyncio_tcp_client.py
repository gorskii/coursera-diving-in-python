""" asyncio, tcp-client
"""

import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001)
    print(f"send: {message}")
    writer.write(message.encode())
    writer.close()


loop = asyncio.get_event_loop()
message = "Hello, World!"
loop.run_until_complete(tcp_echo_client(message))
loop.close()
