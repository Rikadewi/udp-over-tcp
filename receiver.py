import socket
import sys
import function
import threading

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
                    print("Writing File...", "output-" + str(int.from_bytes(identifier, byteorder='big')))
                    function.writeFile(file[int.from_bytes(identifier, byteorder='big')], "output-" + str(int.from_bytes(identifier, byteorder='big')))
        else: # fileSequence[identifier] < sequence
            valid = False

        if valid:
            replyChecksum = function.calculateChecksum(replyType, identifier, sequence, function.convertIntToNByte(0, 2), bytes(0))
            replyPacket = function.createPacket(replyType, identifier, sequence, function.convertIntToNByte(0, 2), replyChecksum, bytes(0))
            senderSock.sendto(replyPacket, (addr, function.LISTEN_PORT))
    else:
        print("Packet checksum is not valid")

if __name__ == "__main__":
    host = "0.0.0.0"
    try:
        listenPort = int(input("Input port : "))
    except:
        print("Invalid port")
        sys.exit()
    
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
        receiverSock.bind((, listenPort))
        print('Socket bind to port:' + str(listenPort))
    except (socket.error):
    	print ('Bind failed. Error Code : ' + str(socket.error))

    while True:    
        packetReceived, (addr, port) = receiverSock.recvfrom(function.MAX_SENT)
        sendPacketThread = threading.Thread(target = processPacket, args = (packetReceived, addr, senderSock))
        sendPacketThread.start()
    receiverSock.close()
    senderSock.close()
