import time
class Motor:
    
    #In order to make motors turn on at same time, I had to
    #make global variables for the motorKit. Using self.motorFunction
    #meant you couldn't turn multiple motors on at the same time.
    global m1
    global m2
    global m3
    global m4
    global m5
    global m6
    global count
    count = 1
    def __init__(self, motorKit, index, initialThrottle):
        self.motorKit = motorKit
        
        #gross code ahead - sorry
        #When init is run, the program runs through the (if index == ..)
        #4 times, then loops back to the beginning (if index == 1). I need
        #these global variables for motors, as stated above, and I needed
        #them to be assigned in the correct order. That's why I have this
        #'count' variable, very poor way to manage the variable assignments
        #and it should be refactored later
        if index == 1:
            self.motorFunction = motorKit.motor1
            if count == 1:
                global count
                global m1
                m1 = motorKit.motor1
                count = 2
                #print(count)
            elif count == 5:
                global count
                global m5
                m5 = motorKit.motor1
                count = 6
                #print(count)
        elif index == 2:
            self.motorFunction = motorKit.motor2
            if count == 2:
                global count
                global m2
                m2 = motorKit.motor2
                count = 3
                #print(count)
            elif count == 6:
                global count
                global m6
                m6 = motorKit.motor2
        elif index == 3:
            self.motorFunction = motorKit.motor3
            if count == 3:
                global count
                global m3
                m3 = motorKit.motor3
                count = 4
                #print(count)
        elif index == 4:
            self.motorFunction = motorKit.motor4
            if count == 4:
                global count
                global m4
                m4 = motorKit.motor4
                count = 5
                #print(count)
        else:
            print("Bad input")#deal with this later :)

        self.prevThrottle = initialThrottle
        

    #Note: I added this motor_num variable because you need
    #different motors turning on for different functions (ie
    #if a joystick is pressed you only want motors 5 and 6
    #responding, if D pad is pressed you want motors 1-4 turning).
    def throttle(self, value, delay, motor_num):
        #print("Prev Throttle " + str(self.prevThrottle))
        print("Value: " + str(value))
        #print("motor num: " + str(motor_num))
        difference = value - self.prevThrottle
        
        #it doesnt let you reach 1.0 or -1.0
        if value == 1.0:
            value = 0.9
        if value == -1.0:
            value = -0.9
        if difference == 0:
            return
        step = round(difference/(abs(difference)*32), 2)
            
        #print("Difference " + str(difference))
        #print("Step " + str(step))
        
        #warning, gross code ahead - sorry 
        if motor_num == 5:
            #I added this (value < 0) check because I needed this interior
            #while loop to stop the prevThrottle from going beyond the
            #limits of [-1, 1]. Now if I have a negative value, lets
            #say -0.9, the prevThrottle will keep getting the step
            #(which will be negative) added until the prevThrottle
            # reaches the value. For example, if value = -0.9, prevThrottle = 0
            # step = -0.1, the step will get added to the throttle
            #until throttle reaches -0.9 (0 -- -0.1 -- ..... -- -0.9)
            if (value < 0):
                while(self.prevThrottle > value):
                    #print("Acceleration " + str(self.prevThrottle)) 
                    self.prevThrottle += step
                    global m5
                    global m6
                    m5.throttle = self.prevThrottle
                    m6.throttle = self.prevThrottle
                    #self.motorFunction.throttle = self.prevThrottle
                    time.sleep(delay)
            #TODO: implement step down to 0 when the value is = 0    
            elif (value == 0.0):
                    self.prevThrottle = 0
                    global m5
                    global m6
                    m5.throttle = self.prevThrottle
                    m6.throttle = self.prevThrottle
            #This will do the same as the top (if value < 0), but it will
            #work for positive values of 'value' instead 
            else: 
                while(self.prevThrottle < value):
                    #print("Acceleration " + str(self.prevThrottle)) 
                    self.prevThrottle += step
                    global m5
                    global m6
                    m5.throttle = self.prevThrottle
                    m6.throttle = self.prevThrottle
                    #self.motorFunction.throttle = self.prevThrottle
                    time.sleep(delay)
                    
        elif motor_num in range(4):
            if (value < 0):
                while(self.prevThrottle >= value):
                    #print("Acceleration " + str(self.prevThrottle)) 
                    self.prevThrottle += step
                    global m1
                    global m2
                    global m3
                    global m4
                    m1.throttle = self.prevThrottle
                    m2.throttle = self.prevThrottle
                    m3.throttle = self.prevThrottle
                    m4.throttle = self.prevThrottle
                    #self.motorFunction.throttle = self.prevThrottle
                    time.sleep(delay)
            elif (value == 0.0):
                print("hello")
                self.prevThrottle = 0
                global m1
                global m2
                global m3
                global m4
                m1.throttle = self.prevThrottle
                m2.throttle = self.prevThrottle
                m3.throttle = self.prevThrottle
                m4.throttle = self.prevThrottle
                time.sleep(delay)
            else: 
                while(self.prevThrottle < value):
                    print("value: " + str(value))
                    #print("throttle: " + str(self.prevThrottle))
                    #print("Acceleration " + str(self.prevThrottle)) 
                    self.prevThrottle += step
                    global m1
                    global m2
                    global m3
                    global m4
                    m1.throttle = self.prevThrottle
                    m2.throttle = self.prevThrottle
                    m3.throttle = self.prevThrottle
                    m4.throttle = self.prevThrottle
                    #self.motorFunction.throttle = self.prevThrottle
                    time.sleep(delay)
                
                    
