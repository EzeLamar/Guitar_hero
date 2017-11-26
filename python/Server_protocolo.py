import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8888)
print('starting up on port',server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

COMIENZO_CARACT=63

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    
    try:
        print('connection from',client_address)

        # Receive the msje in small chunks and retransmit it
        while True:
            msje= connection.recv(8).decode("utf-8") 
            print('received ', msje)
            ##DIVIDO EL MSJE SEGUN LOS SEPARADORES '$'
            camposMsje= msje.split('$')
            print("paquete ",camposMsje)
            ##OBTENGO CAMPO TIPO:
            campoTipo=camposMsje[1]

            ##SEGUN EL TIPO OBTENEMOS (O NO) EL PAYLOAD
            #si el tipo es '0' (TECLAS):
            if campoTipo=='0':
                campoPayload= camposMsje[2][:-1]
                print('es de tipo 0..')
                print(campoPayload)
                #obtenemos la nota correspondiente:
                nroPayload= ord(campoPayload)-COMIENZO_CARACT
                print("el # de nota es: ", nroPayload)
            #si el tipo es '1' (ACTIVAR_POWERUP):
            elif campoTipo=='1':
                print("activo un powerUp")
            elif campoTipo=='2':
                print('es de tipo 2..')
                #obtenemos el volumen correspondiente:
                campoPayload= camposMsje[2][:-1]
                volumen= ord(campoPayload)-COMIENZO_CARACT
                print("el volumen actual es: ",volumen)


            if msje:
                print('waiting next package from client')
                connection.sendall(str.encode(msje))		
            else:
                print('no more data from ', client_address)
                break           
    finally:
        # Clean up the connection
        connection.close()