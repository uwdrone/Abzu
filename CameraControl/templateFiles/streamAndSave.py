import io
import picamera
import socket

class myOutput(object):
    def __init__(self, filename, sock):
        self.output_file = io.open(filename, 'wb')
        self.output_sock = sock.makefile('wb')
        
    def write(self, buf):
        self.output_file.write(buf)
        self.output_sock.write(buf)
        
#        
#HOST = '192.168.1.100' # Enter IP or Hostname of your server
#PORT = 8000 # Pick an open Port (1000+ recommended), must match the server port
##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket()
#address = ('192.168.1.100', 8000)
#sock.bind(address)       
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.100', 8100))

with picamera.PiCamera() as camera:
#    breaks it
#    camera.resolution = (320, 240)
#    camera.framerate = 10
    output = myOutput('/home/pi/Desktop/VideoRecordings/testvideo.h264', sock)
    
    camera.start_recording(output, format = 'h264')
    camera.wait_recording(30)
    camera.stop_recording()
    