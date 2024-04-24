from machine import Pin, PWM

class Motor(object):

    def __init__(self, in1, in2, freq=1000):
        self.freq = freq
        self.sp = 0
        self.p_in1 = PWM(Pin(in1, Pin.OUT), freq=self.freq, duty=self.sp)
        self.p_in2 = PWM(Pin(in2, Pin.OUT), freq=self.freq, duty=self.sp)
        self.p_in1.duty(0)
        self.p_in2.duty(0)

    def stop(self):
        self.p_in1.duty(0)
        self.p_in2.duty(0)

    def forward(self,s=None):
        if s is not None:
            self.sp = min(1023, max(0, s))
        self.p_in2.duty(0)
        self.p_in1.duty(self.sp)

    def reverse(self,s=None):
        if s is not None:
            self.sp = min(1023, max(0, s))
        self.p_in1.duty(0)
        self.p_in2.duty(self.sp)
        
    def speed(self, s=None):
        if s is None:
            return self.sp
        else:
            self.sp = min(1023, max(0, s))
            
class Group(object):
    def __init__(self, in_1_A, in_2_A, in_1_B, in_2_B):
        self.motorA = Motor(in_1_A, in_2_A)
        self.motorB = Motor(in_1_B, in_2_B)
        self.group_speed = 0
    
    def forward(self):
        self.motorA.forward()
        self.motorB.forward()
    
    def reverse(self):
        self.motorA.reverse()
        self.motorB.reverse()
    
    def stop(self):
        self.motorA.stop()
        self.motorB.stop()
        
    def setSpeed(self, speed = None):
        self.motorA.speed(speed)
        self.motorB.speed(speed)
        
        