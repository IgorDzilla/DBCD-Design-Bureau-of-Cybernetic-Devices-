from machine import Pin, PWM

def mapper(x, in_min = 0, in_max = 180, out_min = 20, out_max = 120):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class Servo(object):
    
    def __init__(self, pin, angle = 0, freq = 50):
        self.freq = freq
        self.angle = angle
        self.pin = PWM(Pin(pin, Pin.OUT), freq=self.freq)
        self.pin.duty(0)
    
    def rotate(self, angle):
        if angle < 0 or angle > 180:
            return
        self.angle = angle
        self.pin.duty(mapper(self.angle))