import sys
import random

# Kamus value type in binary
DATA = bin(0x0)[2:]
ACK = bin(0x1)[2:]
FIN = bin(0x2)[2:]
FIN_ACK = bin(0x3)[2:]
MAX_DATA = ((0x1)<<15)*8 #dalam bit

# packet = '0101010101001010101011010010101011010101010101010101010101010101010101010010101010101010101010'

def createListPacket(filename):

    data_raw = openFile(filename)
    data_biner = removeTag(toBiner(data_raw))
    
    tipe =''
    identifier = randomId() 
    sequence = ''
    length = ''
    checksum = ''
    data = ''

    listPacket = []
    
    count_seq= 1
    while(len(data_biner)>MAX_DATA):
        data = data_biner[0:MAX_DATA]
        data_biner = data_biner[MAX_DATA:]
        tipe = convertIntToNBit(getInt(DATA),4) 
        sequence = convertIntToNBit(count_seq,16)
        length = convertIntToNBit(len(data),16)
        checksum = convertIntToNBit(calculateChecksum(tipe, identifier, sequence, length, data),16)
        packet = createPacket(tipe,identifier,sequence,length,checksum,data)
        count_seq+=1
        listPacket.append(packet)

    tipe = convertIntToNBit(getInt(FIN),4) 
    sequence = convertIntToNBit(count_seq,16)
    length = convertIntToNBit(len(data_biner),16)
    checksum = convertIntToNBit(calculateChecksum(tipe, identifier, sequence, length, data_biner),16)
    packet = createPacket(tipe,identifier,sequence,length,checksum,data_biner) 
    listPacket.append(packet)

    return listPacket

# createPacket membentuk sebuah packet berdasarkan parameter yang disediakan
def createPacket(tipe, identifier, sequence, length, checksum, data):
    return tipe + identifier + sequence + length + checksum + data
    
# breakPacket will break a packet to type, id, sequence, length, checksum, and data
def breakPacket(packet):
    tipe = packet[0:4]
    identifier = packet[4:8]
    sequence = packet[8:24]
    length = packet[24:40]
    checksum = packet[40:56]
    data = packet[56:]
    return tipe, identifier, sequence, length, checksum, data

# calculateChecksum return checksum of given parameter
# return integer desimal
def calculateChecksum(tipe, identifier, sequence, length, data):
    packetWOChecksum = tipe + identifier + sequence + length + data    #paket without checksum

    # inisiasi
    piecePacket = packetWOChecksum[0:16]           #Mengambil 16 bits pertama
    packetWOChecksum = packetWOChecksum[16:]      
    calculateCheck = int(piecePacket,2)             
    
    while(len(packetWOChecksum)>16):
        satuanPiecePacket = packetWOChecksum[0:16]
        packetWOChecksum = packetWOChecksum[16:]
        calculateCheck = calculateCheck ^ int(satuanPiecePacket,2)

    #Bit paket tidak kelipatan 16
    jumlahTambahNol =  16-(len(packetWOChecksum))
    
    for x in range(jumlahTambahNol):
        packetWOChecksum += '0'

    calculateCheck = calculateCheck ^ int(packetWOChecksum,2)

    return calculateCheck

# validateChecksum return true or false based on checksum
def validateChecksum(packet):
    #Membuang data checksum dari paket
    tipe, identifier, sequence, length, checksum, data = breakPacket(packet)
    calculateCheck = calculateChecksum(tipe, identifier, sequence, length, data)

    if (calculateCheck == int(checksum,2)):
        return True
    else:
        return False
    
# convertIntToNBit menerima input integer dan menghasilkan binary sepanjang N bit
def convertIntToNBit(integer, n):
    binary = bin(integer)[2:]
    while (len(binary) < n):
        binary = '0' + binary
    return binary

#Membaca file kemudian mengembalikan data dalam format binary
def openFile(filename): 
    data = open(filename,"rb").read()
    return data

#Menguban menjadi biner: 0b000011101010....
def toBiner(dataFile):
    integer=int.from_bytes(dataFile, byteorder=sys.byteorder)
    biner=bin(integer) 
    return biner

#Remove 0b from biner
def removeTag(biner):
    return biner[2:len(biner)]

#Generate Random ID
def randomId():
    return convertIntToNBit(random.randint(0, 15), 4)

#get Integer from biner
def getInt(biner):
    return int(biner,2)


# file = input()
# list=createListPacket(file)
# for packet in list:
#     print(packet)
#     print()






   
