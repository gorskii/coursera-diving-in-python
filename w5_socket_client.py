import socket
import time
import threading
import multiprocessing

CLIENT_COUNT = 1000
WORKER_COUNT = 4


def process_response(client_id, worker_index):
    try:
        with socket.create_connection(("127.0.0.1", 10001), 20) as sock:
            try:
                # time.sleep(5)
                sock.sendall(f"hello from client {client_id} "
                             f"in worker {worker_index}!\n".encode('utf8'))
                time.sleep(2)
                for i in range(1, 5):
                    sock.sendall(f"ping {i}\n".encode('utf8'))
                    data = sock.recv(1024)
                    if not data:
                        print("no answer")
                        break
                    msg = data.decode('utf8')
                    print(msg, i)
                    time.sleep(1)

            except socket.timeout as ex:
                print("send data timeout:", ex)
            except socket.error as ex:
                print("send data error:", ex)
    except ConnectionError as ex:
        print("connection error:", ex)


def worker(worker_index):
    for client_id in range(CLIENT_COUNT):
        th = threading.Thread(target=process_response, args=(client_id,
                                                             worker_index,))
        th.start()


def parallel_connections():
    worker_list = [multiprocessing.Process(target=worker, args=(worker_index,))
                   for worker_index in range(WORKER_COUNT)]
    for w in worker_list:
        w.start()

    for w in worker_list:
        w.join()


if __name__ == '__main__':
    parallel_connections()
