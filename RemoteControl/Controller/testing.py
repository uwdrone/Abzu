"""Simple example showing how to get gamepad events."""

#from __future__ import print_function


from inputs import get_gamepad


def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            #print event
            #print(event.state)
            #print(event.ev_type, event.code, event.state)
            #ev_type = Sync or Absolute
            
            #Joysticks
            if event.code == "ABS_Y":
                print("This is an X direction movement on the LEFT joystick")
            
            if event.code == "ABS_X":
                print("This is a Y direction movement on the RIGHT joystick")
                
            if event.code == "ABS_RY":
                print("This is an X direction movement on the RIGHT joystick")
            
            if event.code == "ABS_RX":
                print("This is a Y direction movement on the RIGHT joystick")
                
            #Buttons
            if event.code == "BTN_SOUTH":
                print("This is pressing the X button")
            
           
            
                


if __name__ == "__main__":
    main()
