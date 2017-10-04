#!/usr/bin/env python3
import time
import sys
import ev3dev.ev3 as ev3

def eprint(*args, **kwargs): # https://stackoverflow.com/a/14981125
    print(*args, file=sys.stderr, **kwargs)

eprint("Hello, world!")

gyro = ev3.Sensor('in3', driver_name='ms-absolute-imu')
eprint(gyro)
assert gyro.connected
gyro.mode = 'TILT'
eprint(gyro.value(0), gyro.value(1), gyro.value(2))
