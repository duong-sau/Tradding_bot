import threading
import time
from multiprocessing import Process, Queue, Pipe

from Test.SocketProcess import create_socket

queue = Queue()
g_parent_conn, g_child_conn = None, None
g_process = None
process_name = 0


def get_data():
    while True:
        data = queue.get()
        if data is None:
            break
        print("Received:", data)


def reconnect_websocket():
    # start process
    print('start socket')
    global process_name, g_process, g_parent_conn, g_child_conn
    local_parent, local_child = Pipe()
    process = Process(target=create_socket, args=(process_name, queue, local_child))
    process.start()
    process_name += 1

    print('run socket')
    # stop old process
    temp_process = g_process
    temp_parent, temp_child = g_parent_conn, g_child_conn
    if not temp_process is None:
        temp_parent.send("1")
        temp_process.terminate()
        temp_process.join()
        temp_process.close()

    # wait
    g_process = process
    g_parent_conn = local_parent
    g_child_conn = local_child
    for i in range(10):
        print(f'run socket {i}')
        time.sleep(1)


if __name__ == '__main__':
    thread = threading.Thread(target=get_data)
    thread.start()

    while True:
        reconnect_websocket()
