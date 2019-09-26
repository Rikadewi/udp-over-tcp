import sys
import random
import time
import math

# Kamus value type in byte
DATA = b'\x00'
ACK = b'\x01'
FIN = b'\x02'
FIN_ACK = b'\x03'

MAX_DATA = 32768 #dalam byte
LISTEN_PORT = 6789
MAX_SENT = 33000
MAX_PROGRESS = 40

def createListPacket(filename):
    data_byte = openFile(filename)
    identifier = randomId()
    listPacket = []
    count_seq= 1

    while(len(data_byte)>MAX_DATA):
        data = data_byte[0:MAX_DATA]
        data_byte = data_byte[MAX_DATA:]
        tipe =  DATA
        sequence = count_seq.to_bytes(2,byteorder ="big")
        length = len(data).to_bytes(2,byteorder="big")
        checksum = calculateChecksum(tipe, identifier, sequence, length, data)
        packet = createPacket(tipe,identifier,sequence,length,checksum,data)
        count_seq+=1
        listPacket.append(packet)

    tipe = FIN
    sequence = count_seq.to_bytes(2,byteorder ="big")
    length = len(data_byte).to_bytes(2,byteorder="big")
    checksum = calculateChecksum(tipe, identifier, sequence, length, data_byte)
    packet = createPacket(tipe,identifier,sequence,length,checksum,data_byte)
    listPacket.append(packet)
    return listPacket


#Input paket dalam byte array
def getID(packet):
    return (packet[0] & 15).to_bytes(1,)

#Generate Random ID return bytearray with lenght 1 byte
def randomId():
    return (random.randint(0, 15)).to_bytes(1, byteorder='big')

# createPacket membentuk sebuah packet berdasarkan parameter yang disediakan
def createPacket(tipe, identifier, sequence, length, checksum, data):
    combine = (int.from_bytes(tipe,byteorder="big") << 4 )| (int.from_bytes(identifier,byteorder="big"))
    tipe_id = combine.to_bytes(1,byteorder="big")
    
    return tipe_id + sequence + length + checksum + data
    
# breakPacket will break a packet to type, id, sequence, length, checksum, and data
def breakPacket(packet):        #packet merupakan bytearray
    tipe = (packet[0] >> 4).to_bytes(1,byteorder='big')
    identifier = (packet[0] & 15).to_bytes(1,byteorder='big')
    sequence = packet[1:3]
    length = packet[3:5]
    checksum = packet[5:7]
    data = packet[7:]
    return tipe, identifier, sequence, length, checksum, data

# calculateChecksum return checksum of given parameter
# return string biner
def calculateChecksum(tipe, identifier, sequence, length, data):
    packetWOChecksum = ((int.from_bytes(tipe,byteorder='big') << 4) + int.from_bytes(identifier,byteorder='big')).to_bytes(1,byteorder='big') + sequence + length + data    #paket without checksum
    # print(packetWOChecksum)

    # inisiasi
    piecePacket = packetWOChecksum[0:2]           #Mengambil 16 bits pertama
    packetWOChecksum = packetWOChecksum[2:]    
    calculateCheck = int.from_bytes(piecePacket,byteorder='big')
    # print(calculateCheck)
    # print(piecePacket)             
    
    while(len(packetWOChecksum)>2):
        satuanPiecePacket = packetWOChecksum[0:2]
        packetWOChecksum = packetWOChecksum[2:]
        calculateCheck = calculateCheck ^ int.from_bytes(satuanPiecePacket,byteorder='big')
        # print(satuanPiecePacket)

    # #Bit paket tidak kelipatan 2
    # jumlahTambahNol =  2-(len(packetWOChecksum))
    
    # for x in range(jumlahTambahNol):
    #     # print(type(packetWOChecksum) + " = tipe paketWOceksam")
    #     packetWOChecksum = packetWOChecksum + str(0)

    # print(packetWOChecksum)
    calculateCheck = calculateCheck ^ int.from_bytes(packetWOChecksum,byteorder='big')
    # print("calculate check" + str(calculateCheck))

    return calculateCheck.to_bytes(2,byteorder='big')

# validateChecksum return true or false based on checksum
def validateChecksum(packet):
    #Membuang data checksum dari paket
    tipe, identifier, sequence, length, checksum, data = breakPacket(packet)
    calculateCheck = calculateChecksum(tipe, identifier, sequence, length, data)

    if int.from_bytes(calculateCheck,byteorder='big') == int.from_bytes(checksum,byteorder='big'):
        return True
    else:
        return False
    
# convertIntToNByte menerima input integer dan menghasilkan arraybyte sepanjang N byte
def convertIntToNByte(integer, n):
    return integer.to_bytes(n, byteorder='big')

#Membaca file kemudian mengembalikan data dalam format byteArray
def openFile(filename): 
    data = open(filename,"rb")
    dataByte = data.read()
    data.close()
    return dataByte

#Menguban menjadi biner: 0b000011101010....
def toBiner(dataFile):
    integer=int.from_bytes(dataFile, byteorder='big')
    biner=bin(integer) 
    return biner

#Remove 0b from biner
def removeTag(biner):
    return biner[2:]

def removeBpetik(paketACK):
    return paketACK[2:(len(paketACK)-1)]

#Generate Random ID return bytearray with lenght 1 byte
def randomId():
    return (random.randint(0, 15)).to_bytes(1, byteorder='big')

#get Integer from biner
def getInt(biner):
    return int(biner,2)

#Menambahkan 0b pada biner
def addTag(binary):
    return '0b' + binary

#Menuliskan file dari type data byte
def writeFile(byte,filename):
    # integer = int(binary,2)
    # byte = integer.to_bytes((integer.bit_length()+7)//8, byteorder='big', signed = False)

    f = open(filename, "wb+")
    f.write(byte)
    f.close()


# f = openFile(input())
# data_biner = removeTag(toBiner(f))
# writeFile(data_biner,"output.pdf")
   
# create an array and initialize with element
def initialize(size, element):
    array = [element] * size
    return array

# create progress bar
# def printProgressBar(i, totalPacket):
#     index = i + 1
#     progressPercentage = math.floor((index/totalPacket)*MAX_PROGRESS)
#     progress = '#'*progressPercentage
#     space = ' '*(MAX_PROGRESS - progressPercentage)
#     if index == totalPacket:
#         endChar = '\n'
#     else:
#         endChar = '\r'
#     print('Progress: [' + progress + space + '] Input Filename', end=endChar)
