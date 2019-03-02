import time
class Motor:
    def __init__(self, motorKit, index, initialThrottle):
        self.motorKit = motorKit
        if index == 1:
            self.motorFunction = motorKit.motor1
        elif index == 2:
            self.motorFunction = motorKit.motor2
        elif index == 3:
            self.motorFunction = motorKit.motor3
        elif index == 4:
            self.motorFunction = motorKit.motor4
        else:
            print("Bad input")#deal with this later :)

        self.prevThrottle = initialThrottle
        
    def throttle(self, value, delay):
        print("Prev Throttle " + str(self.prevThrottle))
        print("Value: " + str(value))
        
        difference = value - self.prevThrottle
        
        if difference == 0:
            return
        
        step = round(difference/(abs(difference)*32), 2)

        print("Difference      " + str(difference))
        print("Step " + str(step))
        
        temp = self.prevThrottle
        
        while(temp != value):
            print("Acceleration " + str(temp))
            
            temp = self.prevThrottle + step
            if temp > value-step and step > 0.0:
                self.prevThrottle = value
                break
            elif temp < value-step and step < 0.0:
                self.prevThrottle = value
                break
            else:
                self.prevThrottle = temp
                self.motorFunction.throttle = temp
                time.sleep(delay)
        
        
