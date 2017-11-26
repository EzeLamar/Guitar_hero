import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8888)
print('connecting to ', server_address)
sock.connect(server_address)

notaActual=0        #[0-255]
volumenActual=5     #[0-10]
COMIENZO_CARACT=63
try:
    while True:    
        # Send data
        time.sleep(0.5)
        msje=sock.recv(8)
        print("recibi un refresco!")
        if msje.decode("utf-8")=="<6$3$>":
            ##PRUEBA PAQUETE TIPO '0' (TECLAS)
            nota= chr(notaActual+32+COMIENZO_CARACT)    #genero un char que representa la nota que voy a mandar.
            campoTT= len(nota.encode("utf-8"))+6
            message = str.encode("<"+str(campoTT)+"$0$"+nota+">")
            print('sending ' ,message)
            print(len(message))

            ##PRUEBA PAQUETE TIPO '2' (VOLUMEN)
            #volumen= chr(volumenActual+COMIENZO_CARACT)
            #message= "<6$2$"+volumen+">"
            #message= message.encode("utf-8")
            

            ##PRUEBA PAQUETE TIPO '1' (ACTIVAR_POWERUP)
            #message= "<6$1$>"
            #message= message.encode("utf-8")

            ##ENVIO EL PAQUETE ARMADO
            sock.sendall(message)
    #        time.sleep(0.1)
            # Look for the response
            

            #cambio al siguiente paquete a enviar..
            notaActual+=1
            if notaActual>31:
                notaActual=0
 #           time.sleep(0.1)

finally:
    print('closing socket')
    sock.close()
