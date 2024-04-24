from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

from utime import sleep
from driver import Motor



motor1 = Motor(25, 26)
motor2 = Motor(27, 14)
motor3 = Motor(21, 19)
motor4 = Motor(17, 16)
speed = 1023
motor1.speed(speed)
motor2.speed(speed)
motor3.speed(speed)
motor4.speed(speed)

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Create a Pin object for the onboard LED, configure it as an output
led = Pin(2, Pin.OUT)

# Initialize the LED state to 0 (off)
led_state = 0
stop_cmds = [b'!B507', b'!B606', b'!B705', b'!B804']

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data) # Print the received data
    if data == b'!B516':
        motor1.forward()
        motor2.forward()
        motor3.forward()
        motor4.forward()
    elif data == b'!B714':
        motor1.forward()
        motor2.reverse()
        motor3.forward()
        motor4.reverse()
    elif data == b'!B813':
        motor1.reverse()
        motor2.forward()
        motor3.reverse()
        motor4.forward()
    elif data == b'!B615':
        motor1.reverse()
        motor2.reverse()
        motor3.reverse()
        motor4.reverse()
    elif data in stop_cmds:
        motor1.stop()
        motor2.stop()
        motor3.stop()
        motor4.stop()

# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception
    