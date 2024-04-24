def forward():
    print("Moving forward")

def reverse():
    print("Moving back")
    
def toRight():
    print("Moving to the right")
    
def toLeft():
    print("Moving to the left")
    
def fullStop():
    print("Full stop")

def grab():
    print("Grabbing")

def release():
    print("Releasing")

def up():
    print("Up")
    
def down():
    print("Down")

def servoStop():
    print("Servo stopping")

functions = {
    b'!B516': forward,
    b'!B813': toRight,
    b'!B714': toLeft,
    b'!B615': reverse,
    b'mstop': fullStop,
    b'!B219': up,
    b'!B417': down,
    b'sstop': servoStop,
    b'!B11:': grab,
    b'!B318': release
}

while True:
    cmd = input("Enter command (or type 'exit' to stop): ")
    if cmd == 'exit':
        break
    cmd = str.encode(cmd)
    
    try:
        functions[cmd]()
    except KeyError:
        print("Invalid command")