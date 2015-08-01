#!/usr/bin/python3
import time
from random import randint
from access_modules import zwave

start_wait_time = randint(1, 20) * 60
time.sleep(start_wait_time)

zwave.set_livingroom_light("ON", False)

on_time = randint(150, 200) * 60
time.sleep(on_time)

zwave.set_livingroom_light("OFF", False)
