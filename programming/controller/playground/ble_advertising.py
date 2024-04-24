from machine import Pin, PWM
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

from utime import sleep
from driver import Motor, Group
from myServo import Servo


#define motors and motor groups
speed = 1023

right = Group(25, 26, 32, 33)
left = Group(16, 17, 18, 19) 
right.setSpeed(speed)
left.setSpeed(speed)

#define servo and start angle
angle = 30
servo_pin = PWM(Pin(23), Pin.OUT)
servo_pin.freq(50)
servo_pin.duty(0)

#define bad servo
lever = PWM(Pin(27), Pin.OUT)
lever.freq(50)
lever.duty(0)

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))
    
servo(servo_pin, angle)
    
# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()
# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)
 
#define commamds
motor_stop_cmds = [b'!B507', b'!B606', b'!B705', b'!B804']
servo_stop_cmds = [b'!B20:', b'!B408']

# Define a callback function to handle received data
def on_rx(cmd):
    global angle
    print("Data received: ", cmd) # Print the received data
    
    #movement commands
    if cmd == b'!B516':
        right.forward()
        left.forward()

    if cmd == b'!B813':
        right.forward()
        left.reverse()
    
    if cmd == b'!B714':
        right.reverse()
        left.forward()
        
    if cmd == b'!B615':
        right.reverse()
        left.reverse()
        
    if cmd in motor_stop_cmds:
        right.stop()
        left.stop()
    
    if cmd == b'!B219':
        lever.duty(60)
        
    if cmd == b'!B417':
        lever.duty(100)
    
    if cmd in servo_stop_cmds:
        lever.duty(0)
    
    if cmd == b'!B11:':
        if angle == 30:
            angle = 85
        print(angle)
        servo(servo_pin, angle)

                
    if cmd == b'!B318': 
        if angle == 85:
            angle = 30
        print(angle)
        servo(servo_pin, angle)
         
        
    
# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception