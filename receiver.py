import socket
import sys
import function

host = "0.0.0.0"
port = 6789

# packet = '0101010101001010101011010010101011010101010101010101010101010101010101010010101010101010101010'

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

# # one thread receiver
# while True:
#     file = ''
#     packetReceived, addr = receiverSock.recvfrom(1024)
#     print ("Message: ", packetReceived)
#     if function.validateChecksum(packetReceived):
#         valid = True
#         tipe, identifier, sequence, length, checksum, data = function.breakPacket(packetReceived) 
#         if tipe == function.DATA:
#             replyType = function.ACK
#         elif tipe == function.FIN:
#             replyType = function.FIN_ACK
#             print("Whole Data Received")
#         else:
#             valid = False
#             print("Packet data type is not valid, data type is " + tipe)
        
#         if valid:
#             replyChecksum = function.calculateChecksum(replyType, identifier, sequence, 0, '')
#             replyPacket = function.createPacket(replyType, identifier, sequence, 0, replyChecksum, '')
#             receiverSock.sendto(replyPacket.encode('utf-8'), addr)
    
#     else:
#         print("Packet checksum is not valid")

# create an array with initialize array
def initialize(size, element):
    array[size]
    for element_array in array:
        element_array = element
    return array

# multithreaded receiver
while True:
    file = initialize(16, '')
    fileSequence = initialize()
    packetReceived, addr = receiverSock.recvfrom(1024)
    print ("Message: ", packetReceived)
    if function.validateChecksum(packetReceived):
        valid = True
        tipe, identifier, sequence, length, checksum, data = function.breakPacket(packetReceived) 
        if tipe == function.DATA:
            replyType = function.ACK
        elif tipe == function.FIN:
            replyType = function.FIN_ACK
            print("Whole Data Received")
        else:
            valid = False
            print("Packet data type is not valid, data type is " + tipe)
        
        if valid:
            replyChecksum = bin(function.calculateChecksum(replyType, identifier, sequence, 0, ''))[2:]
            replyPacket = function.createPacket(replyType, identifier, sequence, 0, replyChecksum, '')
            receiverSock.sendto(replyPacket.encode('utf-8'), addr)
    
    else:
        print("Packet checksum is not valid")

receiverSock.close()
