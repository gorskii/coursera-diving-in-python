import os
import socket
import multiprocessing
import threading

HOST = '127.0.0.1'
PORT = 10001
WORKERS_COUNT = 4


def process_request(conn, addr):
    ip, port = addr
    print(f"connected client {ip}:{port}")
    with conn:
        print("listen...")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode('utf8')
                print(msg)
                if (str(msg).startswith('ping')):
                    conn.sendall("pong".encode('utf8'))
            except socket.timeout as e:
                print("closed by timeout:", e)
                break
            except ConnectionError as e:
                print("connection error:", e)
                break


def worker(sock, host, port):
    print(f"pid {os.getpid()} is listening on {host}:{port}...")
    while True:
        conn, addr = sock.accept()
        print("pid", os.getpid())
        conn.settimeout(10)  # Установка таймаута
        th = threading.Thread(target=process_request, args=(conn, addr))
        th.start()
        print("closed")


def create_socket(host: str, port: int):
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen()

        workers_count = WORKERS_COUNT
        workers_list = [multiprocessing.Process(target=worker,
                                                args=(sock, host, port))
                        for _ in range(workers_count)]

        for w in workers_list:
            w.start()

        for w in workers_list:
            w.join()


if __name__ == '__main__':
    create_socket(HOST, PORT)
