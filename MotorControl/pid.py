import math
from threading import Thread
import socket

##
# Class PID
# PID controller -- with basis conversion defined by angle beta
#
# written by Brady Pomerleau

class PID:
    def __init__(self):
        self.beta = 0.972 #rad
        self.k_p = 0
        self.k_i = 0
        self.k_d = 50
        self.max_i = 100000
        self.min_i = -self.max_i
        self.sum_0 = 0
        self.sum_1 = 0
        self.last_angle = [0.0,0.0]

    # this is the interface to the controller
    # inputs: angle and ref are tuples of angles in the form (pitch roll)
    # outputs: tuple of controller actuation parameters
    def updatePID(self, angle, ref):
        angle = self.convert_cart2cross((angle[0], angle[1]))
        ref = self.convert_cart2cross((ref[0], ref[1]))
        error = (ref[0] - angle[0], ref[1]-angle[1])
        pval = self.P(error)
        ival = self.I(error)
        dval = self.D(angle)
        return (pval[0] + ival[0] + dval[0], pval[1] + ival[1] + dval[1])

    def P(self, error):
        # apply proportional gain
        return (error[0]*self.k_p, error[1]*self.k_p)

    def I(self, error):
        # compute integral
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

        # apply integral gain
        return (self.sum_0 * self.k_i, self.sum_1 * self.k_i)

    def D(self, angle):
        # compute derivative
        dif = (angle[0] - self.last_angle[0], angle[1] - self.last_angle[1])
        self.last_angle[0] = angle[0]
        self.last_angle[1] = angle[1]
        #multiply by k_d
        return (dif[0]*self.k_d, dif[1]*self.k_d)

    # for converting x,y basis into M-basis, specified by angle beta in def __init__
    def convert_cart2cross(self, val):
        pitch = val[0]
        roll = val[1]
        M1 = roll*math.cos(self.beta) + pitch*math.sin(self.beta)
        M2 = roll*math.cos(self.beta) - pitch*math.sin(self.beta)
        return (M1, M2)

