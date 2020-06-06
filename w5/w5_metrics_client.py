""" A client to communicate with metrics storage server using TCP-sockets.
    Allows to send and receive CPU, memory, disk and network usage metrics
    using 'put' and 'get' commands respectively.
"""
from typing import Dict, List, Tuple


class Client:
    def __init__(self, host: str, port: int, timeout: int = None) -> None:
        self._host = host
        self._port = port
        self._timeout = None or timeout

    def get(self, metric: str) -> Dict[str: List[Tuple[int, float]]]:
        pass

    def put(self, metric: str, value: float, timestamp: int = None) -> None:
        pass
