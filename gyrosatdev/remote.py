#!/usr/bin/env python3
import time
import sys
import ev3dev.ev3 as ev3

def eprint(*args, **kwargs): # https://stackoverflow.com/a/14981125
    print(*args, file=sys.stderr, **kwargs)

class gimbal:
    def __init__(self, port, lower_limit, upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
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

    def set_speed_safe(self, speed):
        if(speed >= 0 and self.motor.position >= self.upper_limit) or (speed <= 0 and self.motor.position <= self.lower_limit):
            self.stop()
        else:
            self.set_speed(speed)

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


class remote:
    def __init__(self):
        self.irRemote          = ev3.InfraredSensor()
        self.irRemote.mode     = self.irRemote.MODE_IR_REMOTE 

    def get_button(self):
        return self.irRemote.value(0)

    def none(self):
         return self.get_button() == 0         
    def up_left(self):
        return self.get_button() == 1   
    def down_left(self):
        return self.get_button() == 2   
    def up_right(self):        
        return self.get_button() == 3   
    def down_right(self):
        return self.get_button() == 4   
    def top(self):
        return self.get_button() == 9                                       

class gyro:
    def __init__(self):
        self.sensor          = ev3.GyroSensor()
        self.sensor.mode     = self.sensor.MODE_GYRO_RATE
        self.calibrate_rate()

    def get_rate_raw(self):
        return self.sensor.value(0) 

    def get_rate(self):
        return self.sensor.value(0) - self.offset       

    def calibrate_rate(self):
        total = 0
        count = 20
        interval = 0.05
        eprint('Calibrating Gyro')
        for i in range(0,count):
            total += self.get_rate_raw()
            time.sleep(interval)
        self.offset = round(total/count)
        eprint("Offset: " + str(self.offset))



##########################################################################
##
## MAIN
##
##########################################################################

remote = remote()
gimbal = gimbal('outD',-500,500)
gyro = gyro()

while True:
    if remote.none():
        gimbal.set_speed(0)
    if remote.up_left():
        gimbal.set_speed_safe(500)    
    if remote.down_left():
        gimbal.set_speed_safe(-500)  
    if remote.up_right():
        kp = -10
        gimbal.set_speed_safe(gyro.get_rate()*kp)       
    if remote.top():
        break
    time.sleep(0.1)
