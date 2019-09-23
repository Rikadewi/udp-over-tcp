import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

try:
    receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except (socket.error):    
    print('Failed to create socket. Error Code : ' + socket.error)
    sys.exit()

try:
    receiverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    print('Socket bind to address ' + str(UDP_IP_ADDRESS) + str(UDP_PORT_NO))
except (socket.error):
	print ('Bind failed. Error Code : ' + str(socket.error))
	sys.exit()

while True:
    data, addr = receiverSock.recvfrom(1024)
    print ("Message: ", data)

receiverSock.close()
