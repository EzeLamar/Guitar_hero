import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.21', 8888)
print('starting up on port',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    
    try:
        print('connection from',client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(6).decode("utf-8") 
            print('received ', data)
            if data:
                print('waiting next package from client')
#                connection.sendall(data)		si quisiera contestar...
            else:
                print('no more data from ', client_address)
                break           
    finally:
        # Clean up the connection
        connection.close()