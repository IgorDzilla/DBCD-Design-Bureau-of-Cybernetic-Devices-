"""
UART Service
-------------

An example showing how to write a simple program using the Nordic Semiconductor
(nRF) UART service.

"""

import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from termcolor import colored
from pynput import keyboard

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

#listener for keyboard
press_cmds = {"w": "on", "s": "back", "a": "right", "d": "left"}
release_cmds = {"w": "off", "s": "stop", "a": "stop", "d": "stop"}

button_states = {"w": False, "s": False, "a": False, "d": False}
monitored_buttons = list(button_states)


# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


async def uart_terminal(device_name):
    """This is a simple "terminal" program that uses the Nordic Semiconductor
    (nRF) UART service. It reads from stdin and sends each line of data to the
    remote device. Any data received from the device is printed to stdout.
    """

    def match_nus_uuid(device: BLEDevice, adv: AdvertisementData):
        # This assumes that the device includes the UART service UUID in the
        # advertising data. This test may need to be adjusted depending on the
        # actual advertising data supplied by the device.
        if UART_SERVICE_UUID.lower() in adv.service_uuids:
            return True

        return False

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

        async def on_press(key):
            try:
                if not button_states[key.char] and key.char in monitored_buttons:
                    button_states[key.char] = not button_states[key.char]
                    data = press_cmds[key.char]

                    for s in sliced(data, rx_char.max_write_without_response_size):
                        print(s)
                        await client.write_gatt_char(rx_char, s, response=False)

                    print("Sent:", data)

            except AttributeError:
                return False

        async def on_release(key):
            if key == keyboard.Key.esc:
                return False

            if key.char in button_states:
                print('{0} released'.format(key))
                button_states[key.char] = not button_states[key.char]
                data =  release_cmds[key.char]

                for s in sliced(data, rx_char.max_write_without_response_size):
                    await client.write_gatt_char(rx_char, s, response=False)

                print("sent:", data)

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


def run_terminal(device_name):
    try:
        asyncio.run(uart_terminal(device_name=device_name))
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
'''
if __name__ == "__main__":
    try:
        asyncio.run(uart_terminal())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
'''

run_terminal("mpy-uart")
