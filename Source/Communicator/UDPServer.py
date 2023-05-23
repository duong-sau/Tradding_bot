import socket
from threading import Thread

from Source.Communicator import main_port, main_ip


class UDPServer(Thread):

    def __init__(self, receive_call_back) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((main_ip, main_port))
        self.receive = receive_call_back
        self.running = True

    def run(self) -> None:
        while self.running:
            if self.receive is None:
                continue
            data, server = self.sock.recvfrom(4096)
            data = data.decode()
            self.receive(data)

    def close(self):
        self.sock.close()
        self.running = False
