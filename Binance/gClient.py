import time

public_client = None


def set_client(client):
    global public_client
    public_client = client


def clear_client():
    global public_client
    public_client = None


def get_client():
    global public_client
    while True:
        if public_client is None:
            time.sleep(1)
            continue
        return public_client
