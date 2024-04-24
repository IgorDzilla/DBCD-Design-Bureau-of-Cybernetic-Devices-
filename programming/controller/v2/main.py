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

#define stuff for color detection
i2c_bus = I2C(0, sda=Pin(4), scl=Pin(21))
tcs = TCS34725(i2c_bus)
tcs.gain(4)#gain must be 1, 4, 16 or 60
tcs.integration_time(80)
color=['Cyan','Black','Yellow','Navy','Orange','Green','Red']
col_id = 0

async def color_det():
    global col_id

    rgb=tcs.read(1)
    r,g,b=rgb[0],rgb[1],rgb[2]
    h,s,v=rgb_to_hsv(r,g,b)
    if (h>340)or(h<10):
        col_id=6
    if 10<h<60:
        col_id=4
    if 60<h<120:
        col_id=2
    if 120<h<180:
        col_id=5
    if 180<h<240:
        if v>130:
            col_id=0
        if 30<v<40:
            col_id=3
        if v<30:
            col_id=1
    #print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))
                
async def send_color(int_ms):     
    while True:
        try:
            while True:
                print(color[col_id])
                uart.write(color[col_id]+"\n")
                await asio.sleep_ms(int_ms)
        except KeyboardInterrupt:
            pass

async def execute(int_ms):
    while True:
        try:
            functions[cmd_parser(cmd)]()
        except KeyError:
            pass
        await color_det()
        

print("Starting")
loop = asio.get_event_loop()

#create looped tasks
loop.create_task(execute(5))
loop.create_task(send_color(100))

# loop run forever
loop.run_forever()
