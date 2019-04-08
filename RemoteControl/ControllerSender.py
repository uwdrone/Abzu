import pygame, sys, time    #Imports Modules
from pygame.locals import *
import socket
import signal

def handler(signum, frame):
    s.close()

HOST = '192.168.1.102' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

pygame.init()#Initializes Pygame
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()#Initializes Joystick

# get count of joysticks=1, axes=27, buttons=19 for DualShock 3

joystick_count = pygame.joystick.get_count()
print("joystick_count")
print(joystick_count)
print("--------------")

numaxes = joystick.get_numaxes()
print("numaxes")
print(numaxes)
print("--------------")

numbuttons = joystick.get_numbuttons()
print("numbuttons")
print(numbuttons)
print("--------------")


button_dict = {
    0  : "x_button",
    1  : "circle",
    2  : "triangle",
    3  : "square",
    4  : "L1",
    5  : "R1",
    6  : "L2",
    7  : "R2",
    8  : "Select",
    9  : "Start",
    10 : "PS_Button",
    11 : "L3",
    12 : "R3",
    13 : "D_Up",
    14 : "D_Down",
    15 : "D_Left",
    16 : "D_Right"
}

axis_dict = {
    0 : "LX",
    1 : "LY",
    3 : "RX",
    4 : "RY",
}


prevstr = str()
loopQuit = False
while loopQuit == False:

    #Left Joystick  - X Axis - Axis 0
    #               - Y Axis - Axis 1
    #Right Joystick - X Axis - Axis 3
    #               - Y Axis - Axis 4
    # test joystick axes and prints values
    outstr1 = ""
    #for i in range(0,5):
    for i in [x for x in range(5) if x != 2]:
        axis = round(joystick.get_axis(i), 1)
        axis_name = axis_dict[i]
        outstr1 = outstr1 + axis_name + ":" + str(axis) + "|"
      #  outstr = outstr + str(i) + ":" + str(axis) + "|"
    #print("Joystick axis and values:")
    #print(outstr1)

    # test controller buttons
    outstr2 = ""
    for i in range(0,numbuttons):
        #if i in button_dict:
        #name = button_dict[i]
        #print(name)
        #else:
        button = joystick.get_button(i)
        button_name = button_dict[i]
        #outstr = outstr + str(i) + ":" + str(button) + "|"
        if i == numbuttons-1:
            outstr2 = outstr2 + button_name + ":" + str(button) + "|"
        else:
            outstr2 = outstr2 + button_name + ":" + str(button) + "|"
    #print("Button values:")
    #print(outstr2)

    outstr3 = "".join((outstr1, outstr2))
    
    if outstr3 != prevstr:
        prevstr = outstr3
        print(outstr3)
        s.send(outstr3.encode())
   
    
    for event in pygame.event.get():
       if event.type == QUIT:
           loopQuit = True
       elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
               loopQuit = True
             
       # Returns Joystick Button Motion
       if event.type == pygame.JOYBUTTONDOWN:
        print("joy button down")
       if event.type == pygame.JOYBUTTONUP:
        print("joy button up")
       if event.type == pygame.JOYBALLMOTION:
        print("joy ball motion")
       # axis motion is movement of controller
       # dominates events when used
       if event.type == pygame.JOYAXISMOTION:
           # print("joy axis motion")
           pass


    time.sleep(0.04)
pygame.quit()
sys.exit()
