import time
import datetime
import sys
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_laser_range_finder import BrickletLaserRangeFinder
from threading import Thread

HOST = "192.168.1.17"
PORT = 4223
UID = "uzs"
ipcon = IPConnection()
lrf = BrickletLaserRangeFinder(UID, ipcon)

callback_count = 0
callback_threshold = 12
first = True
cb_time_window = 1
distance = 2790


def start(main_conn):
    ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, cb_connected)
    ipcon.connect(HOST, PORT)
    while True:
        if main_conn.poll():
            cmd = main_conn.recv()
            if cmd == "TERMINATE":
                lrf.disable_laser()
                ipcon.disconnect()
                sys.exit(0)

        time.sleep(0.05)


def evaluate_cb_no():
    global first, callback_count
    time.sleep(cb_time_window)
    if callback_count > callback_threshold:
        now = datetime.datetime.now()
        print("Alarm: ", str(callback_count), str(now))

    callback_count = 0
    first = True


def cb_reached(distance):
    global first, callback_count
    if first:
        th = Thread(target=evaluate_cb_no)
        th.start()
        first = False

    callback_count += 1


def cb_connected(connected_reason):
    print("Connected to stack")
    lrf.set_moving_average(30, 30)
    lrf.set_debounce_period(40)
    lrf.enable_laser()
    time.sleep(0.3)
    lrf.register_callback(lrf.CALLBACK_DISTANCE_REACHED, cb_reached)
    lrf.set_distance_callback_threshold('<', distance, 0)
