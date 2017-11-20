###VER QUE ONDA POR QUE CUANDO COMPARO LOS "1"s Y LOS "0"s  ME DA FALSE!!!!!!! (AGREGAR_CANCION)

##hay que armar un objeto nota que contenga
	#color
	#posicion
	#tamaño

##notasSonando almacena obj notas que aparecen en pantalla
##notas alamacena la cancion, por lo tanto tiene todas las  notas que apareceran en la partida (True) o los silencios (False)

##en el while:
	#por cada tick vemos si debemos agregar una nota nueva a notasSonando.
 	#recorremos el notasSonando y las dibujamos en su correspondiente posicion
 	#chequeamos la 

import pygame, sys, time, _thread, socket
from pygame.locals import *

##----------------SERVIDOR TCP-----------------------
def iniciarServidor(threadName):
	#variable global compartida
	global notaActual

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = ('localhost', 8888)
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
				data = connection.recv(8).decode("utf-8") 
				print(data)
				if data:
					print('waiting next package from client')
					notaActual=int(data)
					connection.sendall(str.encode(data))
				else:
					print('no more data from ', client_address)
					break           
		finally:
			# Clean up the connection
			connection.close()

#def iniciarServidor(threadName):
#	global notaActual
#	while True:
#		print(threadName)
#		notaActual=0
#		time.sleep(1)
#		notaActual=1
#		time.sleep(1)
#		notaActual=2
#		time.sleep(1)
#		notaActual=3
#		time.sleep(1)
#		notaActual=4
#		time.sleep(1)



def convertirAcorde(x):
	acorde=[False,False,False]
	if x in (1, 11,101,111):
		acorde[2]=True
	if x in (10,11,110,111):
		acorde[1]=True
	if x in (100,101,110,111):
		acorde[0]=True
	return acorde

def cargar_cancion():
	cancion=[]
	CANT_NOTAS=3

	with open("pepe.txt", "r") as fichero:
		for linea in fichero:
			acorde=[False,False,False]
#			print(linea)
			#determino que acorde es:
			NroAcorde= int(linea)
			acorde=convertirAcorde(NroAcorde)
			cancion.append(acorde)
#	print(cancion)
	return cancion


class disco_nota:
	color= (0,0,0)
	posx = 0
	posy = 0

def iniciar_juego(threadName):
	global notaActual
	pygame.init()

	#ventana juego
	BACKGROUND = pygame.display.set_mode((400,600), 0, 32)
	pygame.display.set_caption('Guitar Hero')

	#frames per second
	FPS= 20 #FRAMES PER SECOND
	fpsClock = pygame.time.Clock()

	#set up the Colors
	BLACK 	= (0,0,0)
	WHITE 	= (255,255,255)
	GREEN	= (0,255,0)
	RED 	= (255,0,0)
	BLUE 	= (0,0,255)
	##YELLOW 	= ()
	##ORANGE 	=

	#pos ini 	[x,y] 	Discos
	POSINIGREEN= 	(20,0)
	POSINIRED = 	(80,0)
	POSINIBLUE =	(140,0)

	#aca se cargan las notas de una cancion
	notas = cargar_cancion()
	ritmo = 35	#indica que notas hay que cargar en el juego
	notasSonando = []
	contador=0

	#texto notas acertadas 
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 32)
	textSurfacePuntaje = textoPuntajeObj.render(str(contador), True, GREEN, BLUE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (270,100)

	##MUSICA DE FONDO
	pygame.mixer.init()
	pygame.mixer.music.load('pepe.mp3')
	#arranco la musica
	pygame.mixer.music.play(-1,0.0)



	while True:
#		print(threadName)
		#GUI
		BACKGROUND.fill(WHITE)
		textSurfacePuntaje = textoPuntajeObj.render(str(contador), True, GREEN, BLUE)
		BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)
		pygame.draw.line(BACKGROUND,BLACK, (20,0), (20,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (80,0), (80,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (140,0), (140,600), 4)
		#agregar notas
		if ritmo>=0:
			if notas[ritmo][0] == True:
				nota = disco_nota()
				nota.color= GREEN
				nota.posx = POSINIGREEN[0]
				nota.posy = POSINIGREEN[1]
				notasSonando.append(nota)
				
			if notas[ritmo][1] == True:
				nota = disco_nota()
				nota.color= RED
				nota.posx = POSINIRED[0]
				nota.posy = POSINIRED[1]
				notasSonando.append(nota)
				
			if notas[ritmo][2] == True:
				nota = disco_nota()
				nota.color= BLUE
				nota.posx = POSINIBLUE[0]
				nota.posy = POSINIBLUE[1]
				notasSonando.append(nota)
		ritmo+=1
		if ritmo == len(notas):
			ritmo = 0

		aEliminar=[]
		#LOGICA DE MOVIMIENTO
		for nota in notasSonando:
			nota.posy += 20
			if nota.posy >= 600:
				aEliminar.append(nota)
			pygame.draw.circle(BACKGROUND,nota.color, (nota.posx,nota.posy), 20, 0)

		#elimino las notas que ya salieron de la pantalla
		for nota in aEliminar:
			notasSonando.remove(nota)

		pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 4)
		pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 4)
		pygame.draw.circle(BACKGROUND,BLUE, (140,580), 20, 4)

		if notaActual==1:
			pygame.draw.circle(BACKGROUND,BLUE, (140,580), 20, 0)
		if notaActual==2:
			pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
		if notaActual==3:
			pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
			pygame.draw.circle(BACKGROUND,BLUE, (140,580), 20, 0)
		if notaActual==4:
			pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 0)
		
			
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key ==K_z:
					pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 0)
					contador+=1
				if event.key==K_x:
					pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
					contador+=1
				if event.key == K_c:
					pygame.draw.circle(BACKGROUND,BLUE, (140,580), 20, 0)
					contador+=1
			elif event.type == QUIT:
#				print(contador)
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fpsClock.tick(FPS)	##siempre se llama luego del update()


#def reproducirMusica(threadName):
#	##MUSICA DE FONDO
#	pygame.mixer.init()
#	pygame.mixer.music.load('pepe.mp3')
#	#arranco la musica
#	pygame.mixer.music.play(-1,0.0)
#
#	while(True):
#		print(threadName)
#		pass

##-------------------------------------------------------------------------------##

##EJEUTAMOS EN PARALELO SERVER Y EL JUEGO
#variables globales
notaActual =0



#iniciar_juego(0)
try:
	_thread.start_new_thread( iniciar_juego, (0,) )
	_thread.start_new_thread( iniciarServidor, (1,) )
#	_thread.start_new_thread( reproducirMusica, ("Thread-3",) )
except:
   print ("Error: unable to start thread")

while 1:
   pass
