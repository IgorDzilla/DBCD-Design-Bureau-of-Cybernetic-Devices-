from pynput import keyboard

def on_press(key):
    try:
        print(f"Pressed {key.char}")
    except AttributeError:
        print(f"Pressed {key}")

def on_release(key):
    print(f"Released {key}")
    if key ==  keyboard.Key.esc:
        return False

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
