import socket
import sys

import function as pf

# Target IP
host = "10.18.103.22"
# host = "127.0.0.1"

# Target Port
port = 6789

# Message
# Message = "Hello, Willi"
filename = '/test.txt'
listPacket = fungsiLukas('filename')

try:
    senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except (socket.error):    
    print('Failed to create socket. Error Code : ' + socket.error)
    sys.exit()

totalPacket = len(listPacket)
i = 0

while True:
    Message = listPacket[i]
    try :
        senderSock.sendto(Message.encode('utf-8'), (host, port))
        reply, addr = senderSock.recvfrom(1024)
        print("Receiver reply :" + str(reply))
        
    except socket.error:
        print("Failed to send message, Error :" + socket.error)
        sys.exit()

    # while i <
