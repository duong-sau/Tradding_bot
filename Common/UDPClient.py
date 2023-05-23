import socket
import time
from threading import Thread


class UpdClient:

    def __init__(self, ip, port, receive_call_back) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.bind((ip, port))
        self.receive = receive_call_back

    def send_message(self, ip, port, message):
        server_address = (ip, port)
        self.sock.sendto(message.encode(), server_address)

    def listen(self) -> None:
        while True:
            time.sleep(1)
            # data, server = self.sock.recvfrom(4096)
            # print('Dữ liệu phản hồi:', data.decode())
            # self.receive(data.decode())

    def close(self):
        self.sock.close()