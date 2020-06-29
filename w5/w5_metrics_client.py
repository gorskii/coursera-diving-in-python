""" A client to communicate with metrics storage server using TCP-sockets.

Allows to send and receive CPU, memory, disk and network usage metrics
using 'put' and 'get' commands respectively.
"""
import socket
import time
from typing import Dict, List, Tuple

STATUS_OK = 'ok\n'
STATUS_ERROR = 'error\n'
EOL = '\n\n'


class Client:
    def __init__(self, host: str, port: int, timeout: int = None) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout
        self._socket: socket.socket = self._connect()

    def __del__(self) -> None:
        try:
            self._disconnect()
        except AttributeError:
            pass

    def get(self, metric: str) -> Dict[str, List[Tuple[int, float]]]:
        data = f'get {metric}\n'
        try:
            self._socket_write(data)
            response = self._socket_read()
            if (response.startswith(STATUS_OK)
                    and response.endswith(EOL)):
                response = response[len(STATUS_OK):]
                if response == '\n':
                    return {}
                response = response[:-len(EOL)].split('\n')
                metrics = (
                    item.split()
                    for item in response
                )
                metrics_dict = {}
                for key, value, timestamp in metrics:
                    if str(key) in metrics_dict.keys():
                        metrics_dict[str(key)].append(
                            (int(timestamp), float(value))
                        )
                    else:
                        metrics_dict[str(key)] = [
                            (int(timestamp), float(value))
                        ]
                for item in metrics_dict.values():
                    item.sort(key=lambda tuple: tuple[0])
                return metrics_dict
            elif (response.startswith(STATUS_ERROR)
                  and response.endswith(EOL)):
                error_message = response[len(STATUS_ERROR):-len(EOL)]
                raise ClientError(error_message)
            else:
                raise ClientError(f'Invalid response: {response}')
        except (OSError, ConnectionError) as e:
            raise ClientError('Connection error') from e

    def put(self, metric: str, value: float, timestamp: int = None) -> None:
        if timestamp is None:
            timestamp = int(time.time())
        data = f'put {metric} {value} {timestamp}\n'
        try:
            self._socket_write(data)
            response = self._socket_read()
            if (response.startswith(STATUS_OK)
                    and response.endswith(EOL)):
                response = response[len(STATUS_OK):]
                if response == '\n':
                    return
                else:
                    raise ClientError(f'Invalid response: {response}')
            elif (response.startswith(STATUS_ERROR)
                  and response.endswith(EOL)):
                error_message = response[len(STATUS_ERROR):-len(EOL)]
                raise ClientError(error_message)
            else:
                raise ClientError(f'Invalid response: {response}')
        except (OSError, ConnectionError) as e:
            raise ClientError('Connection error') from e

    def _connect(self) -> socket.socket:
        try:
            return socket.create_connection(
                (self._host, self._port),
                self._timeout
            )
        except ConnectionError as e:
            raise ClientError('Connection error') from e

    def _disconnect(self) -> None:
        self._socket.close()
        del self._socket

    def _socket_read(self, bufsize: int = 1024) -> str:
        return self._socket.recv(bufsize).decode('utf8')

    def _socket_write(self, data: str) -> None:
        self._socket.sendall(data.encode('utf8'))


class ClientError(Exception):
    pass
