import os
import sys
import time

from Source.Communicator.UDPServer import UDPServer
from tabulate import tabulate

if __name__ == '__main__':

    devices = {}


    def clear_screen():
        os.system('cls')


    def draw():

        table_data = [(key, value) for key, value in devices.items()]

        table = tabulate(table_data, headers=["DCA", "Ping"], tablefmt="fancy_grid")
        print(table)


    def on_ping_receive(message):
        name = message[6:]
        if name not in devices.keys():
            devices[name] = 5
        else:
            if devices[name] + 1 < 25:
                devices[name] = devices[name] + 5
            else:
                devices[name] = 25


    upd_server = UDPServer(on_ping_receive)
    upd_server.start()

    try:
        while True:
            for device in devices.keys():
                if devices[device] > 0:
                    devices[device] = devices[device] - 1
            clear_screen()
            draw()
            time.sleep(1)
    except:
        upd_server.close()
        sys.exit(1)
