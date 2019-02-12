
import time
from adafruit_motorkit import MotorKit
import socket
from motorStateMachine import Motor
from commandParser import parseMsg

def: motorController:
    HOST = '192.168.1.101' #Server IP
    PORT = 12345 # Pick an open Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #managing error exception
    try:
        s.bind((HOST, PORT))
    except socket.error:
        print("bind failed")

    s.listen(5)

    print("Socket awaiting connections")

    kit = MotorKit() #initialize motor object for first HAT
    kit1 = MotorKit(0x61) #initialize motor object for second HAT, 0x61 i2c adress
    
    (conn, addr) = s.accept()
    print("Connected")

    while True:
        motor1 = Motor(kit, 1) #forward thrust 1
        motor2 = Motor(kit, 2) #forward thrust 2
        motor3 = Motor(kit, 3) #attitude 1 
        motor4 = Motor(kit, 4) #attitude 2

        motor5 = Motor(kit1, 1) #attitude 3
        motor6 = Motor(kit1, 2) #attitude 4
        
        message = conn.recv(1024) #receive message over socket
        command = parseMsg(message) #parse message into motor command tuple
        
        if command[0] == "FULL_STOP":
            #kill all motors
            motor1.throttle(0.0, 0.05)
            #repeat for all motors
        else:
            #joystick input is defined as 4 values (x and y for both joysticks)
            #joystick left is position and right is attitude
            xleft = command[1]
            yleft = command[2]

            xright = command[3]
            yright = command[4]

            motor1.throttle(resolveVector(xleft,yleft,1)*1.0)
            motor2.throttle(resolveVector(xleft,yleft,2)*1.0)

            motor3.throttle(resolveVector(xright,yright,3)*1.0)
            motor4.throttle(resolveVector(xright,yright,4)*1.0)
            motor5.throttle(resolveVector(xright,yright,5)*1.0)
            motor6.throttle(resolveVector(xright,yright,6)*1.0)

            
        
    conn.close() #Close socket
