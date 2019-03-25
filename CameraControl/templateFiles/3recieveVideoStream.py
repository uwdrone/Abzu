import io
import socket
import struct
import subprocess

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

HOST = '192.168.1.100' # Enter IP or Hostname of your server
PORT = 8900 # Pick an open Port (1000+ recommended), must match the server port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    #cmdline = ['vlc', '--demux', 'h264', '-']
    cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin = subprocess.PIPE)
    #file = '/home/pi/Desktop/VideoRecordings/pleasework.h264'
    while True:
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
        
finally:
    connection.close()
    server_socket.close()
    player.terminate()
    
    

