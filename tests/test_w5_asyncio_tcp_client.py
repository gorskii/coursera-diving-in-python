import asyncio
import unittest
from unittest.mock import patch, AsyncMock
from w5.w5_asyncio_tcp_client import tcp_echo_client


class TestAsyncioTcpClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.message = "Hello, World!"
        self.host = "127.0.0.1"
        self.port = 10001

    @patch('asyncio.open_connection',
           side_effect=ConnectionError)
    async def test_tcp_echo_client_connection_with_invalid_port(
            self,
            connection_mock
    ) -> None:
        self.assertEqual(
            'Failed',
            await tcp_echo_client(self.message, self.host, 11312411)
        )

    @patch('asyncio.open_connection',
           return_value=(AsyncMock(asyncio.StreamReader),
                         AsyncMock(asyncio.StreamWriter)))
    async def test_tcp_echo_client_connection(self, connection_mock) -> None:
        self.assertEqual(
            'Success',
            await tcp_echo_client(self.message, self.host, self.port)

        )


if __name__ == '__main__':
    unittest.main()
