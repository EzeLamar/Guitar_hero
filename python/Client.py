import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8888)
print('connecting to ', server_address)
sock.connect(server_address)

notaActual=0
try:
    while True:    
        # Send data
        message = str.encode(str(notaActual))
        print('sending ' ,message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received ' ,data)

        #cambio al siguiente paquete a enviar..
        notaActual+=1
        if notaActual>4:
            notaActual=0
        time.sleep(0.1)

finally:
    print('closing socket')
    sock.close()
