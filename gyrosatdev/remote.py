#!/usr/bin/env python3
import time
import sys
import ev3dev.ev3 as ev3

def set_speed(motor, speed):
    motor.speed_sp = speed
    motor.run_forever()

def waitforstall():
    while not gimbal.STATE_STALLED in gimbal.state:
        time.sleep(0.01)    

def eprint(*args, **kwargs): # https://stackoverflow.com/a/14981125
    print(*args, file=sys.stderr, **kwargs)

gimbal  = ev3.MediumMotor('outD')

set_speed(gimbal, 200)
time.sleep(0.5)
waitforstall()

set_speed(gimbal, -200)
time.sleep(0.5)
waitforstall()
set_speed(gimbal, 0)

eprint("Hello, world!")
