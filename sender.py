import socket
import sys
import function
import time
import threading

# Target IP
# host = "10.18.103.22"
host = "127.0.0.1"

# Target Port
port = 6789

filename = 'test.txt'
listPacket = function.createListPacket(filename)

try:
    senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("OPEN SOCKET")
except (socket.error):    
    print('Failed to create socket. Error Code : ' + socket.error)
    sys.exit()

totalPacket = len(listPacket)
i = 0
print("Total packet = " + str(totalPacket))

isSuccess = threading.Condition()

def sendPacket(packet, i):
    try :
        isTimeOut = False
        isGetReply = False

        def waitForReply():
            reply = ''
            while not isTimeOut and not isGetReply:
                reply, addr = senderSock.recvfrom(1024)
                if len(reply) != 0:
                    isGetReply = True
            if not isGetReply:
                sendPacket(packet)
            else:
                if(cekPacket(totalPacket,packet,reply)):        
                    print("Packet ke- " +i+ " sampai")
                    isSuccess.notify()
                else:
                    print("Resending packet ke-", + i)
                    sendPacket(packet)

        def waitFiveSeconds():
            time.sleep(.500)
            isTimeOut = True        
                    
        senderSock.sendto(packet.encode('utf-8'), (host, port))

        threading.Thread(target = waitForReply, args = ())
        threading.Thread(target = waitFiveSeconds, args = ())
        
    except socket.error:
        print("Failed to send message, Error :" + socket.error)
        sys.exit()

while True:
    while(i<totalPacket):
        isSuccess.acquire()
        print("Sending packet ke-" + str(i))
        packet = listPacket[i]
        sendPacket(packet, i+1)
        isSuccess.wait()
        i+=1
        isSuccess.release()


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


