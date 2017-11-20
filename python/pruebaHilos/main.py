#!/usr/bin/python3
import func1
import _thread
import time

# Define a function for the thread


def convertirAcorde(x):
	acorde=[False,False,False]
	if x in (1, 11,101,111):
		acorde[2]=True
	if x in (10,11,110,111):
		acorde[1]=True
	if x in (100,101,110,111):
		acorde[0]=True
	return acorde


def cargar_cancion(threadName, delay):
	global glob
	cancion=[]
	CANT_NOTAS=3

	with open("pepe.txt", "r") as fichero:
		for linea in fichero:
			acorde=[False,False,False]
			print ("%s: %s" % ( threadName, linea ))		
#			time.sleep(delay)
			#determino que acorde es:
			NroAcorde= int(linea)
			acorde=convertirAcorde(NroAcorde)
			if NroAcorde==100:
				glob=False
			cancion.append(acorde)
#	print(cancion)


def iniciarServidor(threadName, notaActual,activarPoder, velocidad):
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
					#connection.sendall(data)		si quisiera contestar...
				else:
					print('no more data from ', client_address)
					break           
		finally:
			# Clean up the connection
			connection.close()


def print_time( threadName, delay):
	global glob
	count = 0
	while count < 1000:
#		time.sleep(delay)
		count += 1
		if glob==True:
			print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
		else:
			print("me cagaron")

# Create two threads as follows
glob =True
try:
	_thread.start_new_thread( cargar_cancion, ("Thread-1", 2) )
	_thread.start_new_thread( print_time, ("Thread-2", 4) )
except:
   print ("Error: unable to start thread")

while 1:
   pass