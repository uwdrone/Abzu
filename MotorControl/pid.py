import math
from threading import Thread
import socket

class PID:
    '''
        Maintains the stability of the drone using a PID control system scheme.
        The drone is kept within the plane specified by user input 'ref' by actuating
        based on imu reading and previous state.
    '''
    def __init__(self):
        self.beta = 0.972 #rad
        self.k_p = 0.1
        self.k_i = 0.1
        self.k_d = 0.4
        self.max_i = 100000
        self.min_i = -self.max_i
        self.sum_0 = 0
        self.sum_1 = 0
        self.last_angle = [0.0,0.0]

    def updatePID(self, angle, ref):
        '''
            Interface to stickSteering.
            Inputs: angle: (imu roll, imu pitch), ref: (user roll, user pitch)
            Outputs: the actuation value for the positive motor on the motor cross1 and cross2
        '''
        angle = self.convert_cart2cross((angle[0], angle[1]))
        ref = self.convert_cart2cross((ref[0], ref[1]))
        error = (ref[0] - angle[0], ref[1]-angle[1])
        pval = self.P(error)
        ival = self.I(error)
        dval = self.D(angle)
        cross1 = pval[0] + ival[0] + dval[0]
        cross2 = pval[1] + ival[1] + dval[1]

        if cross1 > 1.0:
            cross1 = 1.0
        elif cross1 < -1.0:
            cross1 = -1.0
        else:
            pass
        if cross2 > 1.0:
            cross2 = 1.0
        elif cross2 < -1.0:
            cross2 = -1.0
        else:
            pass
        return (round(cross1,1), round(cross2,1))

    def P(self, error):
        '''
            Applies the proportional gain to the signal.
        '''
        return (error[0]*self.k_p, error[1]*self.k_p)

    def I(self, error):
        '''
            Computes the integral and applies the integral gain
            to the signal.
        '''
        self.sum_0 += error[0]
        self.sum_1 += error[1]

        if self.sum_0 > self.max_i:
            self.sum_0 = self.max_i
        elif self.sum_0 < self.min_i:
            self.sum_0 = self.min_i

        if self.sum_1 > self.max_i:
            self.sum_1 = self.max_i
        elif self.sum_1 < self.min_i:
            self.sum_1 = self.min_i

        return (self.sum_0 * self.k_i, self.sum_1 * self.k_i)

    def D(self, angle):
        '''
            Takes the derivative and applies the derivative gain to the
            signal.
        '''
        dif = (angle[0] - self.last_angle[0], angle[1] - self.last_angle[1])
        self.last_angle[0] = angle[0]
        self.last_angle[1] = angle[1]

        return (dif[0]*self.k_d, dif[1]*self.k_d)

    def convert_cart2cross(self, val):
        '''
            Converts the pitch and roll angles given in x, y basis to the
            motor cross basis specified by angle beta.
        '''
        pitch = val[0]
        roll = val[1]
        M1 = roll*math.cos(self.beta) + pitch*math.sin(self.beta)
        M2 = roll*math.cos(self.beta) - pitch*math.sin(self.beta)
        return (M1, M2)
