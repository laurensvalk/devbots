#!/usr/bin/env python3
import time
import sys
import ev3dev.ev3 as ev3

def eprint(*args, **kwargs): # https://stackoverflow.com/a/14981125
    print(*args, file=sys.stderr, **kwargs)

class gimbal:
    def __init__(self, port):
        self.motor = ev3.MediumMotor('outD')
        self.set_speed(200)
        self.wait_for_stall()
        self.stop()
        self.motor.position = 0
        self.goto_motor_angle_at_speed(-600, 300)
        self.motor.position = 0                  

    def get_motor_angle(self):
        return self.motor.position    

    def wait_for_completion(self):
        while self.motor.STATE_RUNNING in self.motor.state:
            time.sleep(0.01) 

    def set_speed(self, speed):
        self.motor.speed_sp = speed
        self.motor.run_forever()

    def stop(self):
        self.motor.command = 'stop'      

    def goto_motor_angle_at_speed(self, target_angle, speed):
        speed = abs(speed)
        current_angle = self.motor.position
        if target_angle < current_angle:
            speed = -speed
        self.motor.speed_sp = speed
        self.motor.position_sp = target_angle
        self.motor.command = 'run-to-abs-pos'
        self.wait_for_completion()

    def wait_for_stall(self):
        while not self.motor.STATE_STALLED in self.motor.state:
            time.sleep(0.01)   


gimbal = gimbal('outD')
gimbal.goto_motor_angle_at_speed(500,300)
gimbal.goto_motor_angle_at_speed(0,300)
eprint(gimbal.get_motor_angle())
