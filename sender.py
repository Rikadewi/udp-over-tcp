import socket
import sys
import function
import time
import threading

# Target IP
# host = "10.18.103.22"

# def sendPacket(packet, i):
#     try :
#         isTimeOut = False

#         print("tes")
#         def waitForReply():
#             reply = ''
#             print("wait reply")
#             isGetReply = False
#             while not isTimeOut and not isGetReply:
#                 reply, addr = senderSock.recvfrom(1024)
#                 if len(reply) != 0:
#                     isGetReply = True
#             if not isGetReply:
#                 sendPacket(packet)
#             else:
#                 if(cekPacket(totalPacket,packet,reply)):        
#                     print("Packet ke- " +i+ " sampai")
#                     isSuccess.notify()
#                 else:
#                     print("Resending packet ke-", + i)
#                     sendPacket(packet)

#         def waitFiveSeconds():
#             print("sleep")
#             time.sleep(.500)
#             isTimeOut = True        
                    
#         senderSock.sendto(packet.encode('utf-8'), (host, port))
#         print(packet)
#         print("open thread")
#         waitReplyThread = threading.Thread(target = waitForReply, args = ())
#         sleepThread = threading.Thread(target = waitFiveSeconds, args = ())

#         waitReplyThread.start()
#         sleepThread.start()

#         print("selesai thread")
#     except socket.error:
#         print("Failed to send message, Error :" + socket.error)
#         sys.exit()



# isSuccess = threading.Condition()

# while True:
#     while(i<totalPacket):
#         isSuccess.acquire()
#         print("Sending packet ke-" + str(i+1))
#         # print(listPacket[i])
#         packet = listPacket[i]
#         sendPacket(packet, i+1)
#         isSuccess.wait()
#         i+=1
#         isSuccess.release()

# Fungsi untuk mengecek paket reply
# Memeberikan True jika hasil ceksum untuk reply benar, dan setiap tipe, id, dan sequence memberikan nilai yang benar
def cekPacket(totalPacket, packet, reply):
    tipeSender, identifierSender, sequenceSender, lengthSender, checksumSender, dataSender = function.breakPacket(packet)
    tipeReply, identifierReply, sequenceReply, lengthReply, checksumReply, dataReply = function.breakPacket(reply)

    if((int(sequenceReply,2)<totalPacket) and (int(tipeReply,2)==int(function.ACK,2)) and (int(tipeSender,2)==int(function.DATA))):                 #Bukan paket terakhir
        if(function.validateChecksum(reply)):                                                   #Mengecek Checksum paket
            if(identifierSender==identifierSender and sequenceSender==sequenceACK):             #Mengecek id dan sequence paket sender dengan reply
                return True
            else:
                return False
        else:
            return False
    elif ((int(sequenceReply, 2) == totalPacket) and (tipeReply == function.FIN_ACK) and (tipeSender == function.FIN)):       #Paket terakhir 
        if(function.validateChecksum(reply)):                                                   #Mengecek Checksum paket
            if(identifierSender==identifierSender and sequenceSender==sequenceACK):             #Mengecek id dan sequence paket sender dengan reply
                return True
            else:
                return False
        else:
            return False
    else:
        return False


# def kirimPacket(packet):
if __name__ == "__main__":
    host = "127.0.0.1"
    # Target Port
    portSender = 6889
    portReceiver = 6888

    filename = 'test.txt'
    listPacket = function.createListPacket(filename)

    try:
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiveSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket sender opened")
    except (socket.error):    
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:
        # receiveSock.setblocking(False)
        receiveSock.bind((host, portSender))
        print('Socket bind to address ' + str(host) + ':' + str(portSender))
    except (socket.error):
        print ('Bind failed. Error Code : ' + str(socket.error))

    totalPacket = len(listPacket)
    i = 0
    print("Total packet = " + str(totalPacket))

    while True:
        while(i<totalPacket):
            packet = listPacket[i]
            print("Message = " + packet)
            start = time.time()
            senderSock.sendto(packet.encode('utf-8'), (host, portReceiver))
            (reply, addr) = receiveSock.recvfrom(1024)
            print("asdas")
            end = time.time()
            timeout= end-start

            while(timeout <= 0.5 and not cekPacket(totalPacket, packet, reply)):
                reply, addr = receiveSock.recvfrom(1024)
                end = time.time()
                timeout= end-start

            #timeout atau cekpaket benar
            if(cekPacket(totalPacket,packet,reply)):
                i+=1


