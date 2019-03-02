import socket

HOST = '192.168.1.101' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((host,PORT))
s.connect((HOST,PORT))

from inputs import get_gamepad
#Lets loop awaiting for your input
prev = 0
while True:
    
    #events is a list
    events = get_gamepad()
    
    #command = events
    for event in events:
        if (event.ev_type == "Absolute"):
            num = event.state
        
    
    temp1 = prev - 2
    temp2 = prev + 2
    
    if (num > temp2 or num < temp1):
        string = str(num)
        s.send(string)
    prev = num
    print "prev: " + str(prev)

     #   if (string != temp)
      #      temp = string
            #print(event.state)    #command = raw_input('Enter your command: ')
    #s.send(command)
    #reply = s.recv(1024)
    #if reply == 'Terminate':
    #    break
    #print reply
