#!/usr/bin/env python3
import time
import sys
import ev3dev.ev3 as ev3

########################################################################
## File I/O functions
########################################################################

# Function for fast reading from sensor files
def FastRead(infile):
    infile.seek(0)    
    return(int(infile.read().decode().strip()))

# Function for fast writing to motor files    
def FastWrite(outfile,value):
    outfile.truncate(0)
    outfile.write(str(int(value)))
    outfile.flush()    

# Debug print
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Function to set the duty cycle of the motors
def SetDuty(motorDutyFileHandle, duty):
    # Compansate for nominal voltage and round the input
    dutyInt = int(round(duty))

    # Add or subtract offset and clamp the value between -100 and 100
    if dutyInt > 0:
        dutyInt = min(100, dutyInt)
    elif dutyInt < 0:
        dutyInt = max(-100, dutyInt)

    # Apply the signal to the motor
    FastWrite(motorDutyFileHandle, dutyInt)

########################################################################
## One-time Hardware setup
########################################################################

# EV3 Brick
powerSupply = ev3.PowerSupply()
buttons = ev3.Button()

# Gyro Sensor setup. Possibly make this more generic to better support more sensors.
try: # Set LEGO gyro to Gyro Rate mode, if attached
    gyroSensor          = ev3.GyroSensor()
    gyroSensor.mode     = gyroSensor.MODE_GYRO_RATE
    gyroType            = 'LEGO-EV3-Gyro'
except: # Assume HiTechnic Gyro is attached if LEGO Gyro not found
    gyroSensor          = ev3.Sensor(address="ev3-ports:in2")
    gyroType            = 'HITECHNIC-NXT-Gyro'

# Open gyro rate sensor value file
gyroSensorValueRaw  = open(gyroSensor._path + "/value0", "rb")   

# Touch Sensor setup
touchSensor         = ev3.TouchSensor()
touchSensorValueRaw = open(touchSensor._path + "/value0", "rb")

# Configure the motors
motorLeft  = ev3.LargeMotor('outD')
motorRight = ev3.LargeMotor('outB')    

# Reset the motors
motorLeft.reset()                   # Reset the encoder
motorRight.reset()
motorLeft.run_direct()              # Set to run direct mode
motorRight.run_direct() 

# Open sensor files for (fast) reading
motorEncoderLeft    = open(motorLeft._path + "/position", "rb")    
motorEncoderRight   = open(motorRight._path + "/position", "rb")           

# Open motor files for (fast) writing
motorDutyCycleLeft = open(motorLeft._path + "/duty_cycle_sp", "w")
motorDutyCycleRight= open(motorRight._path + "/duty_cycle_sp", "w")

confirmDutyCycleLeft   = open(motorLeft._path + "/duty_cycle_sp", "rb")  

########################################################################
## Main Test Code
########################################################################

import random
random.seed()

for i in range(100000):
    # duty = (random.random()-0.5)*20
    duty = 20
    written = int(round(duty))
    SetDuty(motorDutyCycleLeft, duty)
    readback = FastRead(confirmDutyCycleLeft)
    if readback != written:
        eprint("Wrote:" + str(written) + " but read: " + str(readback))
    time.sleep(0.004)

SetDuty(motorDutyCycleLeft, 0)