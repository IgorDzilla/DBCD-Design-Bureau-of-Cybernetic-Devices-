import uart_terminal as ut
import discover
from termcolor import colored
from pynput import keyboard


print(colored('Starting terminal\n', 'green'))

print(colored('Starting advertising\n', 'green'))
discover.run_discovery()

print(colored('Enter device name: ', 'green'), end = '')
device_name = str(input())

print("Trying to connect to", device_name)

ut.run_terminal(device_name)
