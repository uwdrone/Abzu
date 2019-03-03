"""Simple unit test for the motor state machine"""
from adafruit_motorkit import MotorKit
from motorStateMachine import Motor

if __name__=="__main__":
    kit = MotorKit()

    motor1 = Motor(kit, 1)
    #motor1.throttle(0.0,0.005)
    kit.motor1.throttle = 0.0
    motor2 = Motor(kit, 2)
    #motor2.throttle(1.0,0.01)

    #motor2.throttle(1.0,0.05)
    motor2.throttle(0.0,0.05)
