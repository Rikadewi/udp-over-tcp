import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

try:
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error, msg:    
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

try:
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    print('Socket bind to address ' + UDP_IP_ADDRESS + UDP_PORT_NO)
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

while True:
    data, addr = serverSock.recvfrom(1024)
    print "Message: ", data)

serverSock.close()
