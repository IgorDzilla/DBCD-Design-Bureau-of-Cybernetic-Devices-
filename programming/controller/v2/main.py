from machine import Pin, PWM, I2C
from ble_uart_peripheral import *
import uasyncio as asio
from time import sleep, sleep_ms
from tcs34725 import *

from movement import *

#bluetooth setup
cmd = ''
state = False
def on_rx():
    global cmd
    cmd = uart.read().decode().strip()
    state = True
    print("Command:", cmd)


ble = bluetooth.BLE()
uart = BLEUART(ble, name="DBCD")
uart.irq(handler=on_rx)

async def execute(int_ms):
    while True:
        try:
            functions[cmd_parser(cmd)]()
        except KeyError:
            pass
        

print("Starting")
loop = asio.get_event_loop()

#create looped tasks
loop.create_task(execute(0))

# loop run forever
loop.run_forever()
