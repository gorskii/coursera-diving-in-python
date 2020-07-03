from unittest import TestCase

from w5.w5_metrics_client import Client


class TestClient(TestCase):
    def setUp(self) -> None:
        self.host = "127.0.0.1"
        self.port = 8888
        self.client = Client(self.host, self.port, timeout=10)

    def test_create_connection(self):
        from socket import socket
        self.assertIsInstance(self.client._socket, socket)

    def test_get_all_metrics(self):
        self.client.put("palm.cpu", 0.5, 1150864247)
        self.client.put("palm.cpu", 0.5, 1150864248)
        self.client.put("palm.cpu", 0.7, 1150864248)
        self.client.put("eardrum.cpu", 3.0, 1150864250)
        self.client.put("eardrum.cpu", 4.0, 1150864251)
        self.client.put("eardrum.memory", 4200000.0, 1503320872)
        expected = {
            'palm.cpu': [
                (1150864247, 0.5),
                (1150864248, 0.7)
            ],
            'eardrum.cpu': [
                (1150864250, 3.0),
                (1150864251, 4.0)
            ],
            'eardrum.memory': [
                (1503320872, 4200000.0)
            ]
        }
        self.assertEqual(expected, self.client.get("*"))

    def test_get_one_metric(self):
        import time
        self.client.put("palm.cpu", 0.5, 1150864247)
        self.client.put("palm.cpu", 0.5, 1150864248)
        self.client.put("palm.cpu", 0.5)
        expected = {
            'palm.cpu': [
                (1150864247, 0.5),
                (1150864248, 0.5),
                (int(time.time()), 0.5)
            ]
        }
        self.assertEqual(expected, self.client.get("palm.cpu"))

    def test_get_nonexistent_metric(self):
        self.assertEqual({}, self.client.get("apricot.cpu"))

    def test_get_invalid_response(self):
        from w5.w5_metrics_client import ClientError
        self.assertRaises(ClientError, self.client.get, "triggering command")

    def test_put_single_metric_with_timestamp(self):
        metric_key = "palm.cpu"
        metric_value = 0.5
        metric_timestamp = 1150864247
        self.client.put(metric_key, metric_value, metric_timestamp)
        expected = (metric_timestamp, metric_value)
        self.assertIn(expected, self.client.get(metric_key)[metric_key])

    def test_put_single_metric_without_timestamp(self):
        import time
        metric_key = "palm.cpu"
        metric_value = 0.5
        metric_timestamp = int(time.time())
        self.client.put(metric_key, metric_value)
        expected = (metric_timestamp, metric_value)
        self.assertIn(expected, self.client.get(metric_key)[metric_key])
