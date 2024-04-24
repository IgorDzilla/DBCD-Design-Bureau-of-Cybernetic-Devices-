from pynput import keyboard

while True:
    with keyboard.Events() as events:
        event = events.get()
        print(event.key)
        if event.key == keyboard.Key.esc:
            break