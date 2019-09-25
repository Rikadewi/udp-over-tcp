import socket
import sys
import function
import threading

listen_port = 4568

def processPacket(packetReceived, addr, senderSock):
    if function.validateChecksum(packetReceived):
        valid = True
        tipe, identifier, sequence, length, checksum, data = function.breakPacket(packetReceived) 
        if fileSequence[int.from_bytes(identifier, byteorder='big')] >= int.from_bytes(sequence, byteorder='big'):
            if tipe == function.DATA:
                replyType = function.ACK
            elif tipe == function.FIN:
                replyType = function.FIN_ACK
            else:
                valid = False
                print("Packet data type is not valid, data type is " + str(tipe))

            if  valid and fileSequence[int.from_bytes(identifier, byteorder='big')] == int.from_bytes(sequence, byteorder='big'):
        
                file[int.from_bytes(identifier, byteorder='big')]+=data
                fileSequence[int.from_bytes(identifier, byteorder='big')]+=1
                if replyType == function.FIN_ACK:
                    # print('write  to file')
                    function.writeFile(file[int.from_bytes(identifier, byteorder='big')], "output-" + str(int.from_bytes(identifier, byteorder='big')))
        else: # fileSequence[identifier] < sequence
            valid = False

        if valid:
            replyChecksum = function.calculateChecksum(replyType, identifier, sequence, function.convertIntToNByte(0, 2), bytes(0))
            replyPacket = function.createPacket(replyType, identifier, sequence, function.convertIntToNByte(0, 2), replyChecksum, bytes(0))
            senderSock.sendto(replyPacket, (addr, listen_port))
    else:
        print("Packet checksum is not valid")

if __name__ == "__main__":
    host = "127.0.0.1"
    senderPort = 1234

    file = function.initialize(16, bytes(0))
    fileSequence = function.initialize(16, 1)
    try:
        receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Socket created')
    except (socket.error):    
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:
        receiverSock.bind((host, function.LISTEN_PORT))
        print('Socket bind to address ' + str(host) + ':' + str(function.LISTEN_PORT))
    except (socket.error):
    	print ('Bind failed. Error Code : ' + str(socket.error))

    while True:    
        packetReceived, (addr, port) = receiverSock.recvfrom(function.MAX_SENT)
        # print("cek valid:")
        # print
        # print(function.validateChecksum(packetReceived))
        # processPacket(packetReceived, addr, senderSock)
        sendPacketThread = threading.Thread(target = processPacket, args = (packetReceived, addr, senderSock))
        sendPacketThread.start()
    receiverSock.close()
    senderSock.close()

# if __name__ == "__main__":
#     while True:
#         try:
#             receiveFileThread = threading.Thread(target=)