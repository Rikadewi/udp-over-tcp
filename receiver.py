import socket
import sys
import function
import threading

host = "127.0.0.1"
port = 6789

try:
    receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except (socket.error):    
    print('Failed to create socket. Error Code : ' + socket.error)
    sys.exit()

try:
    receiverSock.bind((host, port))
    print('Socket bind to address ' + str(host) + ':' + str(port))
except (socket.error):
	print ('Bind failed. Error Code : ' + str(socket.error))

# create an array with initialize array
def initialize(size, element):
    array = [element] * size
    return array


file = initialize(16, '')
fileSequence = initialize(16, 1)

def processPacket(packetReceived, addr):
    print ("Message: ", packetReceived)
    if function.validateChecksum(packetReceived):
        valid = True
        tipe, identifier, sequence, length, checksum, data = function.breakPacket(packetReceived) 
        if fileSequence[identifier] >= sequence:
            if tipe == function.DATA:
                replyType = function.ACK
            elif tipe == function.FIN:
                replyType = function.FIN_ACK
                print("Whole Data Received")
            else:
                valid = False
                print("Packet data type is not valid, data type is " + tipe)
            
            if  valid and fileSequence[identifier] == sequence:
                file[identifier]+=data
                fileSequence[identifier]+=1
                if replyType == function.FIN_ACK:
                    function.writeFile(file[identifier], "output" + identifier)

        else: # fileSequence[identifier] < sequence
            valid = False

        if valid:
            replyChecksum = bin(function.calculateChecksum(replyType, identifier, sequence, 0, ''))[2:]
            replyPacket = function.createPacket(replyType, identifier, sequence, 0, replyChecksum, '')
            receiverSock.sendto(replyPacket.encode('utf-8'), addr)
    
    else:
        print("Packet checksum is not valid")

while True:    
    packetReceived, addr = receiverSock.recvfrom(1024)
    threading.Thread(target = processPacket, args = (packetReceived, addr))
    
receiverSock.close()
