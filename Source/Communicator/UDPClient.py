import socket
import time

from Source.Communicator import main_ip, main_port


class UPDClient:

    def __init__(self, name) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.name = name

    def send_ping(self):
        while True:
            self.send_message(main_ip, main_port, f"ping: {self.name}")
            time.sleep(1)

    def send_message(self, ip, port, message):
        server_address = (ip, port)
        message = str(message)
        self.sock.sendto(message.encode(), server_address)

    def close(self):
        self.sock.close()
