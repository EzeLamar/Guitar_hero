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

import pygame, sys, os, time, threading, socket
from pygame.locals import *

##----------------SERVIDOR TCP-----------------------
def iniciarServidor():
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
					time.sleep(0.01)
				else:
					pass
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

def cargar_cancion(NOMBRE_CANCION):
	cancion=[]
	CANT_NOTAS=3

	with open(NOMBRE_CANCION+'.txt', "r") as fichero:
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

def iniciar_juego():
	global notaActual

	pygame.init()

	N_RITMOS = 18
	
	##INDICAMOS LA CANCION A TOCAR:
	NOMBRE_CANCION= input('ingrese la cancion a tocar: ')

	#obtenemos Ruta donde se encuentran las canciones:
	FILEDIR = os.path.dirname(os.path.realpath('__file__'))
	FILESONGS = FILEDIR+'/canciones/'


	#ventana juego
	BACKGROUND = pygame.display.set_mode((400,600), 0, 32)
	pygame.display.set_caption('Guitar Hero')
	#frames per second
	FPS= 20 #FRAMES PER SECOND
	fpsClock = pygame.time.Clock()
	MOV_Y=20

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
	notas = cargar_cancion(FILESONGS+NOMBRE_CANCION)
	ritmo = 0	#indica que notas hay que cargar en el juego
	notasSonando = []
	contador=0

	#texto notas acertadas 
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 32)
	textSurfacePuntaje = textoPuntajeObj.render(str(contador), True, GREEN, BLUE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (270,100)

#	##MUSICA DE FONDO
	musicaReproduciendo=False
	pygame.mixer.init()
	pygame.mixer.music.load(FILESONGS+NOMBRE_CANCION+'.mp3')

	##CARTEL 3..2..1..GO!
	time.sleep(1)
	print('preparado...')
	time.sleep(1)
	print('listo..')
	time.sleep(1)
	print('ROCK!')


	while True:
#		print(ritmo)
		
		#arranco la musica luego de N ritmos
		if ritmo==N_RITMOS and not musicaReproduciendo:
			print('comienza la musica!')
			pygame.mixer.music.play(-1,0.0)
			musicaReproduciendo= True

		#GUI
		BACKGROUND.fill(WHITE)
		textSurfacePuntaje = textoPuntajeObj.render(str(fpsClock.get_fps()), True, GREEN, BLUE)
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
			nota.posy += MOV_Y
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
				print('good bye')
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fpsClock.tick_busy_loop(FPS)	##siempre se llama luego del update()

##-------------------------------------------------------------------------------##

##EJEUTAMOS EN PARALELO SERVER Y EL JUEGO
#variables globales
notaActual =0

##-------HILOS---------
juegoH = threading.Thread(name='Juego', target=iniciar_juego)
serverH = threading.Thread(name='Server', target=iniciarServidor)

serverH.setDaemon(True)
juegoH.setDaemon(True)

serverH.start()
juegoH.start()

juegoH.join()
serverH.join()


