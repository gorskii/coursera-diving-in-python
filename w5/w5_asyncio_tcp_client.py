""" asyncio, tcp-client
"""

import asyncio


async def tcp_echo_client(message: str, host: str, port: int) -> str:
    status = 'Failed'
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except ConnectionError:
        print(f"{status}: Host {host}:{port} is unreachable")
        return status
    print(f"send: {message}")
    try:
        writer.write(message.encode())
        status = 'Success'
    finally:
        writer.close()
    return status


def main():
    loop = asyncio.get_event_loop()
    message = "Hello, World!"
    host = "127.0.0.1"
    port = 10001
    loop.run_until_complete(tcp_echo_client(message, host, port))
    loop.close()


if __name__ == '__main__':
    main()
