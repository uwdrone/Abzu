import pygame, sys, time    #Imports Modules
from pygame.locals import *

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

loopQuit = False
while loopQuit == False:

    # test joystick axes and prints values
    outstr = ""
    for i in range(0,4):
        axis = joystick.get_axis(i)
        outstr = outstr + str(i) + ":" + str(axis) + "|"
        print("Joystick axis and values:")
        print(outstr)

    # test controller buttons
    outstr = ""
    for i in range(0,numbuttons):
           button = joystick.get_button(i)
           outstr = outstr + str(i) + ":" + str(button) + "|"
    print("Button values:")
    print(outstr)

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

    time.sleep(0.01)
pygame.quit()
sys.exit()
