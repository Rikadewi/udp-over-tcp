import socket
import sys
import function
import time
import threading

listen_port = 4568

# Fungsi untuk mengecek paket reply
# Memeberikan True jika hasil ceksum untuk reply benar, dan setiap tipe, id, dan sequence memberikan nilai yang benar
def cekPacket(totalPacket, packet, reply):
    if reply == bytes(0):
        return False
    
    tipeSender, identifierSender, sequenceSender, lengthSender, checksumSender, dataSender = function.breakPacket(packet)
    tipeReply, identifierReply, sequenceReply, lengthReply, checksumReply, dataReply = function.breakPacket(reply)

    if(int.from_bytes(sequenceReply,byteorder='big')<totalPacket) and tipeReply == function.ACK and tipeSender == function.DATA :                 #Bukan paket terakhir
        if(function.validateChecksum(reply)):                                                   #Mengecek Checksum paket
            if(identifierSender == identifierReply and sequenceSender == sequenceReply):             #Mengecek id dan sequence paket sender dengan reply
                return True
            else:
                return False
        else:
            return False
    elif ((int.from_bytes(sequenceReply, byteorder='big') == totalPacket) and (tipeReply == function.FIN_ACK) and (tipeSender == function.FIN)):       #Paket terakhir 
        if(function.validateChecksum(reply)):                                                   #Mengecek Checksum paket
            if(identifierSender==identifierReply and sequenceSender==sequenceReply):             #Mengecek id dan sequence paket sender dengan reply
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# send a file to host
def sendFile(host, filename, senderSock, receiverSock):
    try:    
        listPacket = function.createListPacket(filename)
    except IOError:
        print("File not found")
        return

    totalPacket = len(listPacket)
    i = 0

    while(i < totalPacket):
        packet = listPacket[i]
        start = time.time()
        try:
            senderSock.sendto(packet, (host, function.LISTEN_PORT))
        except socket.error:
            print("Error in sending packet")
        
        try:
            reply, (addr, port) = receiverSock.recvfrom(function.MAX_SENT)
        except socket.error:
            pass
        end = time.time()
        timeout = end - start
        reply = bytes(0)
        while(timeout <= 0.5 and not cekPacket(totalPacket, packet, reply)):
            try:
                reply, (addr, port) = receiverSock.recvfrom(function.MAX_SENT)
            except socket.error:
                pass
            end = time.time()
            timeout= end-start
        if(cekPacket(totalPacket,packet,reply)):
            i+=1
    print("All packet sent from ", filename)
    
        
if __name__ == "__main__":
    host = "127.0.0.1"
    try:
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket sender opened")
    except (socket.error):    
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()
    try:
        receiverSock.setblocking(False)
        receiverSock.bind((host, listen_port))
        print('Socket bind to address ' + str(host) + ':' + str(listen_port))
    except (socket.error):
        print ('Bind failed. Error Code : ' + str(socket.error))
        sys.exit()

    while True:
        filename = input("Input filename : ")
        try:
            sendFileThread = threading.Thread(target=sendFile, args=(host, filename, senderSock, receiverSock))
        except:
            print ("Unable to start new thread")
        sendFileThread.start()
        
    receiverSock.close()
    senderSock.close()
