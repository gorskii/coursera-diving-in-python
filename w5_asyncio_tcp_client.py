""" asyncio, tcp-client
"""

import asyncio


async def tcp_echo_client(message, loop):
    pass


loop = asyncio.get_event_loop()
message = "Hello, World!"
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
