from machine import Pin
from utime import sleep
import driver

print("Hello, ESP32!")

motor1 = driver.Motor(23, 22)

led = Pin(2, Pin.OUT)

while True:
    motor1.forward()
    led.on()
    sleep(1)
    motor1.stop()
    motor1.reverse()
    led.off()
    sleep(1)