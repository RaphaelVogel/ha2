import time
import sys
import logging
from tinkerforge.ip_connection import IPConnection


HOST = "192.168.1.17"
PORT = 4223
UID = "uzs"
ipcon = IPConnection()
logger = logging.getLogger("ha_logger")


def start(main_conn):
    ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, cb_connected)
    ipcon.connect(HOST, PORT)
    while True:
        if main_conn.poll():
            cmd = main_conn.recv()
            if cmd == "TERMINATE":
                ipcon.disconnect()
                sys.exit(0)

        time.sleep(0.05)


def cb_connected(connected_reason):
    print("Connected to stack")
