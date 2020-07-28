import asyncio
from collections import defaultdict
from typing import Dict, Tuple, List

HOST = "127.0.0.1"
PORT = 8888

SUPPORTED_COMMANDS = ("get", "put")

STATUS_OK = "ok\n"
STATUS_ERROR = "error\n"
EOL = "\n\n"

metrics_dict: Dict[str, List[Tuple[int, float]]] = defaultdict(list)


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        print(self.transport.get_extra_info("peername"))

    def data_received(self, data: bytes) -> None:
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def process_data(data: str) -> str:
    if data.startswith(SUPPORTED_COMMANDS) and data.endswith("\n"):
        try:
            command, metric = data.rstrip("\r\n").split(maxsplit=1)
            if command == SUPPORTED_COMMANDS[0]:
                if " " not in metric:
                    return get_metric(metric)
            if command == SUPPORTED_COMMANDS[1]:
                metric_key, metric_value, timestamp = metric.split()
                return put_metric(
                    metric_key, float(metric_value), int(timestamp)
                )
        except ValueError:
            pass
    return f"{STATUS_ERROR}wrong command{EOL}"


def get_metric(metric_key: str) -> str:
    result = ""
    if metric_key == "*":
        for key, values in metrics_dict.items():
            for value_tuple in sorted(values, key=lambda x: x[0]):
                result += f"{key} {value_tuple[1]} {value_tuple[0]}\n"
    else:
        if metric_key in metrics_dict.keys():
            for value_tuple in sorted(metrics_dict[metric_key],
                                      key=lambda x: x[0]):
                result += f"{metric_key} {value_tuple[1]} {value_tuple[0]}\n"
    return f"{STATUS_OK}{result}\n"


def put_metric(metric_key: str, metric_value: float, timestamp: int) -> str:
    for i, value_tuple in enumerate(metrics_dict[metric_key]):
        if value_tuple[0] == timestamp:
            metrics_dict[metric_key].pop(i)
            break
    metrics_dict[metric_key].append((timestamp, metric_value))
    return f"{STATUS_OK}\n"


def run_server(host: str, port: int) -> None:
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server(HOST, PORT)
