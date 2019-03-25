import io
import socket
import struct
import time
import picamera


HOST = '192.168.1.100' # Enter IP or Hostname of your server
PORT = 8300# Pick an open Port (1000+ recommended), must match the server port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

#port2 = 8900
#
#client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket2.connect((HOST,port2))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
#connection2 = client_socket2.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
#    camera.framerate = 24
#    
#    camera.start_recording(connection, format = 'h264')
#    camera.wait_recording(10)
#    camera.stop_recording()

    start = time.time()
    stream = io.BytesIO()
    
    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell()))
        #connection2.write(struct.pack('<L', stream.tell()))
        connection.flush()
        #connection2.flush()
        
        stream.seek(0)
        connection.write(stream.read())
        #connection2.write(stream.read())
        if time.time()- start > 15:
            break
        
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack('<L', 0))
    #connection2.write(struct.pack('<L', 0))
        
finally:
    connection.close()
    #connection2.close()
    client_socket.close()
    #client_socket2.close()