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
        #print("Prev Throttle " + str(self.prevThrottle))
        print("Value: " + str(value))
        
        difference = value - self.prevThrottle
        
        if difference == 0:
            return
        
##        #it doesnt let you reach 1.0 or -1.0
##        if value == 1.0:
##            value = 0.9
##        if value == -1.0:
##            value = -0.9
##        if difference == 0:
##            return
        step = round(difference/(abs(difference)*32), 2)

        print("Difference " + str(difference))
        print("Step " + str(step))
        
        temp = self.prevThrottle
        
        while(temp != value):
            print("Acceleration " + str(temp))
            
            temp += step
            if temp > 1.0 or temp < -1.0:
                break
            
            self.prevThrottle = temp
            self.motorFunction.throttle = temp
            time.sleep(delay)
        
        
