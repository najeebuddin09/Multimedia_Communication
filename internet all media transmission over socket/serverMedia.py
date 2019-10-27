# this receive video and audio from one client and then broadcast it to the other connected clients

#
# Imports
#

# for sockets
from socket import socket, AF_INET, SOCK_STREAM

# for multithreading
from threading import Thread

# to convert the received data from strings to orignal format
import struct

#
# Globals
#

# Host address i.e the address the server is running on
HOST = input("Enter Host IP\n")

# Port for video transmission
PORT_VIDEO = 3000

# Port for audio transmission
PORT_AUDIO = 4000

#
lnF = 640*480*3

#
CHUNK = 1024

# audio data to be received from clients
BufferSize = 4096

# for storing the addresses of clients for audio tansmission
addressesAudio = {}

#
addresses = {}

#
threads = {}

#
# Function Definitions
#

#
def ConnectionsVideo():
    while True:
        try:
            # accept connection from client for video transmission
            clientVideo, addr = serverVideo.accept()
            print("{} is connected!!".format(addr))

            # store the address of clients
            addresses[clientVideo] = addr
            if len(addresses) > 1:
                for sockets in addresses:
                    if sockets not in threads:
                        threads[sockets] = True
                        # inform the client to start transmission
                        sockets.send(("start").encode())
                        # create thread for video transmission
                        Thread(target=ClientConnectionVideo, args=(sockets, )).start()
            else:
                continue
        except:
            continue

# Accept a connection from client for audio and then create a thread for audio broadcasting of that client to other clients
def ConnectionsSound():
    while True:
        try:
            # accept connection
            clientAudio, addr = serverAudio.accept()
            print("{} is connected!!".format(addr))

            # storing the address of each client
            addressesAudio[clientAudio] = addr

            # Create a thread to start sound transmission
            Thread(target=ClientConnectionSound, args=(clientAudio, )).start()
        except:
            continue

# receive data from clients and then send it to other clients
def ClientConnectionVideo(clientVideo):
    while True:
        try:
            lengthbuf = recvall(clientVideo, 4)
            length, = struct.unpack('!I', lengthbuf)
            recvall(clientVideo, length)
        except:
            continue

# receive audio from client and then broadcast it to other clients
def ClientConnectionSound(clientAudio):
    while True:
        try:
            data = clientAudio.recv(BufferSize)
            broadcastSound(clientAudio, data)
        except:
            continue

# receive function for receiving video data
def recvall(clientVideo, BufferSize):
        databytes = b''
        i = 0
        while i != BufferSize:
            to_read = BufferSize - i
            if to_read > (1000 * CHUNK):
                databytes = clientVideo.recv(1000 * CHUNK)
                i += len(databytes)
                broadcastVideo(clientVideo, databytes)
            else:
                if BufferSize == 4:
                    databytes += clientVideo.recv(to_read)
                else:
                    databytes = clientVideo.recv(to_read)
                i += len(databytes)
                if BufferSize != 4:
                    broadcastVideo(clientVideo, databytes)
        print("YES!!!!!!!!!" if i == BufferSize else "NO!!!!!!!!!!!!")
        if BufferSize == 4:
            broadcastVideo(clientVideo, databytes)
            return databytes

def broadcastVideo(clientSocket, data_to_be_sent):
    for clientVideo in addresses:
        if clientVideo != clientSocket:
            clientVideo.sendall(data_to_be_sent)

# broadcast audio to other clients
def broadcastSound(clientSocket, data_to_be_sent):
    for clientAudio in addressesAudio:
        # send to all clients except the one who send it
        if clientAudio != clientSocket:
            clientAudio.sendall(data_to_be_sent)

serverVideo = socket(family=AF_INET, type=SOCK_STREAM)
try:
    serverVideo.bind((HOST, PORT_VIDEO))
except OSError:
    print("Server Busy")

serverAudio = socket(family=AF_INET, type=SOCK_STREAM)
try:
    serverAudio.bind((HOST, PORT_AUDIO))
except OSError:
    print("Server Busy")

#
# "__main__"
#

# listen for Audio connections from clients. 2 = backlog
serverAudio.listen(2)
print("Waiting for connection..")

# Creating a thread for sound transmission
AcceptThreadAudio = Thread(target=ConnectionsSound)
AcceptThreadAudio.start()

# listening for video connection from clients. 2 = backlog
serverVideo.listen(2)
print("Waiting for connection..")

# Creating a thread for video transmission
AcceptThreadVideo = Thread(target=ConnectionsVideo)
AcceptThreadVideo.start()

# waiting for video thread to complete
AcceptThreadVideo.join()

# closing socket for video transmission
serverVideo.close()
