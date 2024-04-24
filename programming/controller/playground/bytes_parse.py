cmd_1 = b'!B507'
motor_stop_cmds = [b'!B507', b'!B606', b'!B705', b'!B804']

cmd_2 = b'!B20:'
servo_stop_cmds = [b'!B20:', b'!B408']
    
def cmd_parser(cmd):
    if cmd in motor_stop_cmds:
        cmd = b'mstop'

    elif cmd in servo_stop_cmds:
        cmd = b'sstop'
    
    return cmd

print(cmd_parser(cmd_1), cmd_parser(b'nothing'))