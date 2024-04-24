from machine import Pin, PWM
from driver import Motor, Group
from myServo import Servo

#define motors
speed = 1023
right = Group(25, 26, 32, 33)
left = Group(16, 17, 18, 19) 
right.setSpeed(speed)
left.setSpeed(speed)

#define servos
servo = Servo(23, angle=30)
lever = PWM(Pin(27), Pin.OUT)
lever.freq(50)
lever.duty(0)

#define stop cmds
motor_stop_cmds = ['!B507', '!B606', '!B705', '!B804']
servo_stop_cmds = ['!B20:', '!B408']

def forward():
   right.forward()
   left.forward()

def reverse():
    right.reverse()
    left.reverse()
    
def toRight():
    right.forward()
    left.reverse()
    
def toLeft():
    right.reverse()
    left.forward()
    
def fullStop():
    right.stop()
    left.stop()

def grab():
    if servo.angle == 30:
        servo.angle = 85
    servo.rotate(servo.angle)

def release():
    if servo.angle == 85:
        servo.angle = 30
    servo.rotate(servo.angle)

def leverUp():
    lever.duty(60)
    
def leverDown():
    lever.duty(100)

def leverStop():
   lever.duty(0)

def cmd_parser(cmd):
    if cmd in motor_stop_cmds:
        cmd = 'mstop' #stop motor

    elif cmd in servo_stop_cmds:
        cmd = 'lstop' #stop the lever
    
    return cmd

functions = {
    '!B516': forward,
    '!B813': toRight,
    '!B714': toLeft,
    '!B615': reverse,
    'mstop': fullStop,
    '!B219': leverUp,
    '!B417': leverDown,
    'lstop': leverStop,
    '!B11:': grab,
    '!B318': release
}