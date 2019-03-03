import socket

HOST = '192.168.1.101' # Server IP or Hostname
host = socket.gethostname()
hostName = socket.gethostbyname('0.0.0.0')
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print 'Bind failed '
s.listen(5)
print s.getsockname()
print 'Socket awaiting messages'
(conn, addr) = s.accept()
print 'Connected'
    
# awaiting for message
while True:
    data = conn.recv(1024)
    print data
conn.close() # Close connections
