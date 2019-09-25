import socket
import sys
import function
import threading

    
# create an array with initialize array
def initialize(size, element):
    array = [element] * size
    return array

def processPacket(packetReceived, addr):
    packetReceived = function.removeBpetik(str(packetReceived))
    print ("Message: ", packetReceived)
    if function.validateChecksum(packetReceived):
        valid = True
        tipe, identifier, sequence, length, checksum, data = function.breakPacket(packetReceived) 
        if fileSequence[int(identifier,2)] >= int(sequence,2):
            if int(tipe,2) == int(function.DATA,2):
                replyType = function.ACK
            elif int(tipe,2) == int(function.FIN,2):
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
            senderSock.sendto(replyPacket.encode('utf-8'), addr)
    else:
        print("Packet checksum is not valid")


if __name__ == "__main__":
    # print("hai")

    host = "127.0.0.1"
    portSender = 6889
    portReceive = 6888

    file = initialize(16, '')
    fileSequence = initialize(16, 1)
    try:
        receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Socket created')
    except (socket.error):    
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:
        receiverSock.bind((host, portReceive))
        print('Socket bind to address ' + str(host) + ':' + str(portReceive))
    except (socket.error):
    	print ('Bind failed. Error Code : ' + str(socket.error))

    while True:    
        packetReceived, addr = receiverSock.recvfrom(1024)
        sendPacketThread = threading.Thread(target = processPacket, args = (packetReceived, addr))
        sendPacketThread.start()
    receiverSock.close()