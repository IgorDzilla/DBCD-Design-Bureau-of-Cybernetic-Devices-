class Motor:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        
        
        def forward(self):
            self.pin1.value(0)
            self.pin2.value(1)
            
        def backward(self):
            self.pin1.value(1)
            self.pin.value(0)
            
        