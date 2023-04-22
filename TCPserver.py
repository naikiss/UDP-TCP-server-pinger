from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 12000))
serverSocket.listen(1)
print("Started TCP server on port 12000")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    while True:
        message = connectionSocket.recv(1024)
        if not message:
            break
        message = message.upper()
        connectionSocket.send(message)

    connectionSocket.close()
