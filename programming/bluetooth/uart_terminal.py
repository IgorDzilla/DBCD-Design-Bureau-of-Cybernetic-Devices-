import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from termcolor import colored

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


async def uart_terminal(device_name):
    
    device = await BleakScanner.find_device_by_name(device_name)

    if device is None:
        print(colored("Failed to connect.", "red"))
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print(colored("Device was disconnected, goodbye.", "green"))
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        print("received:", data)

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        print(colored("Connected, start typing and press ENTER...", "green"))

        loop = asyncio.get_running_loop()
        nus = client.services.get_service(UART_SERVICE_UUID)
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

        while True:
            print(">>> ", end = "")
            data = input().encode()
            data = data + b'\n'

            if not data:
                break

            for s in sliced(data, rx_char.max_write_without_response_size):
                await client.write_gatt_char(rx_char, s, response=False)

            print("sent:", data)


def run_terminal(device_name):
    try:
        asyncio.run(uart_terminal(device_name=device_name))
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
