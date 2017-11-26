##FALTA:
	#COLISIONES
	#CONTAR CUANTAS NOTAS SEGUIDAS SE ACERTARON
		#MULTIPLICADOR :P
	#VICTORIA/DERROTA 

##notasSonando almacena obj notas que aparecen en pantalla
##notas alamacena la cancion, por lo tanto tiene todas las  notas que apareceran en la partida (True) o los silencios (False)

##en el while:
	#por cada tick vemos si debemos agregar una nota nueva a notasSonando.
 	#recorremos el notasSonando y las dibujamos en su correspondiente posicion
 	#chequeamos la 

import pygame, sys, os, time, threading, socket
from pygame.locals import *


def actualizarVolumen(cantVol, BACKGROUND):
	BLACK= (0,0,0)
	WHITE= (255,255,255)
	X_INICIAL=320 
	Y_INICIAL=200
	
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 32)
	textSurfacePuntaje = textoPuntajeObj.render("vol: "+str(cantVol), True, BLACK, WHITE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	##con esto actualizo
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)


def actualizarLuces(cantEncendidas, BACKGROUND):
	BLUE= (0,0,255)
	MAX_LUCES=4
	RADIO=10
	ESPACIO_ENTRE_LUCES=RADIO*2

	X_INICIAL=300 
	Y_INICIAL=30
	if cantEncendidas>4:
		cantEncendidas=4

	for i in range(1,MAX_LUCES+1):
		pos_x= X_INICIAL+ESPACIO_ENTRE_LUCES*i
		if i<=cantEncendidas:
			pygame.draw.circle(BACKGROUND,BLUE, (pos_x,Y_INICIAL) , RADIO, 0)
		else:
			pygame.draw.circle(BACKGROUND,BLUE, (pos_x,Y_INICIAL) , RADIO, 4)

##----------------SERVIDOR TCP-----------------------
def iniciarServidor():
	#variable global compartida
	global notaActual
	global volumen
	global powerUp_activado
	global powerUp_cant

	COMIENZO_CARACT=63

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = ('192.168.0.4', 8888)
	print('starting up on port',server_address)
	sock.bind(server_address)

	# Listen for incoming connections
	sock.listen(1)
	while True:
		# Wait for a connection
#		print('waiting for a connection')
		connection, client_address = sock.accept()
		try:
#			print('connection from', client_address)
			# Receive the data in small chunks and retransmit it
			while True:
#				time.sleep(0.1)
				refresco_msje="<6$3$>"
				connection.sendall(refresco_msje.encode("utf-8"))
				print('waiting next package from client')
					
				msje= connection.recv(9).decode("utf-8") 
				print('received ', msje)
				
				if msje:
					##DIVIDO EL MSJE SEGUN LOS SEPARADORES '$'
					camposMsje= msje.split('$')
					print("paquete ",camposMsje)
					##OBTENGO CAMPO TIPO:
					campoTipo=camposMsje[1]

					##SEGUN EL TIPO OBTENEMOS (O NO) EL PAYLOAD
					#si el tipo es '0' (TECLAS):
					if campoTipo=='0':
						campoPayload= camposMsje[2][:-1]
#						print('es de tipo 0..')
#						print(campoPayload)
						#obtenemos la nota correspondiente:
						nroPayload= ord(campoPayload)-COMIENZO_CARACT
#						print("el # de nota es: ", nroPayload)
						notaBinaria= convertirBinario(nroPayload)
						##SACO EL ULTIMO BIT YA QUE ESE ES EL DEL RASGUIDO
						rasguido= notaBinaria[:1]
						if rasguido=='1':
							acordeBinario= notaBinaria[1:]
							notaActual=convertirAcordeBinario(acordeBinario)
#							print("rasguido!")
						elif rasguido=='0':
							notaActual=[False,False,False,False,False]

					#si el tipo es '1' (ACTIVAR_POWERUP):
					elif campoTipo=='1':
						pass
#						print("activo un powerUp")
					elif campoTipo=='2':
						pass
#						print('es de tipo 2..')
						#obtenemos el volumen correspondiente:
						campoPayload= camposMsje[2][:-1]
						volumen= ord(campoPayload)-COMIENZO_CARACT
#						print("el volumen actual es: ",volumen)

					##LE CONTESTO AL CLIENTE PARA QUE ENVIE EL SIGUIENTE PAQUETE
					#print('waiting next package from client')
					#connection.sendall(str.encode(msje))
							
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

def convertirBinario(x):
	notaBinaria='{0:06b}'.format(x)
	return notaBinaria

def convertirAcordeBinario(acordeBinario):
	acorde=[False,False,False,False,False]
	if acordeBinario[:1]=='1':
		acorde[0]=True
	if acordeBinario[:2][1:]=='1':
		acorde[1]=True
	if acordeBinario[:3][2:]=='1':
		acorde[2]=True
	if acordeBinario[:4][3:]=='1':
		acorde[3]=True
	if acordeBinario[:5][4:]=='1':
		acorde[4]=True
	return acorde

def cargar_cancion(NOMBRE_CANCION):
	cancion=[]
	CANT_NOTAS=3

	with open(NOMBRE_CANCION+'.txt', "r") as fichero:
		for linea in fichero:
			acorde=[False,False,False,False,False]
#			print(linea)
			#determino que acorde es:
			NroAcorde= linea
			acorde=convertirAcordeBinario(NroAcorde)
#			print(acorde)
			cancion.append(acorde)
#	print(cancion)
	return cancion


class disco_nota:
	color= (0,0,0)
	posx = 0
	posy = 0

def iniciar_juego():
	##VARIABLES GLOBAlES
	global notaActual
	global volumen
	global powerUp_activado
	global powerUp_cant
	global multiplicador


	##valores por defecto de globales
	notaActual=[False,False,False,False,False]
	volumen=5
	powerUp_activado=False
	powerUp_cant=0
	multiplicador =1

	##locales
	cantAcertadas=0
	cantErradas =0


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
	YELLOW 	= (255,215,0)
	ORANGE 	= (255,69,0)

	#pos ini 	[x,y] 	Discos
	POSINIGREEN= 	(20,0)
	POSINIRED = 	(80,0)
	POSINIYELLOW =	(140,0)
	POSINIBLUE =	(200,0)
	POSINIORANGE =	(260,0)

	#aca se cargan las notas de una cancion
	notas = cargar_cancion(FILESONGS+NOMBRE_CANCION)
	ritmo = 0	#indica que notas hay que cargar en el juego
	notasSonando = []
	contador=0

	#texto notas acertadas 
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 32)
	textSurfacePuntaje = textoPuntajeObj.render(str(contador), True, GREEN, BLUE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (280,100)

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

		##--------------------GUI----------------------------
		#VENTANA
		BACKGROUND.fill(WHITE)
		textSurfacePuntaje = textoPuntajeObj.render(str(fpsClock.get_fps()), True, GREEN, BLUE)
		BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)
		pygame.draw.line(BACKGROUND,BLACK, (20,0), (20,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (80,0), (80,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (140,0), (140,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (200,0), (200,600), 4)
		pygame.draw.line(BACKGROUND,BLACK, (260,0), (260,600), 4)


		pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 4)
		pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 4)
		pygame.draw.circle(BACKGROUND,YELLOW, (140,580), 20, 4)
		pygame.draw.circle(BACKGROUND,BLUE, (200,580), 20, 4)
		pygame.draw.circle(BACKGROUND,ORANGE, (260,580), 20, 4)
		

		
		#LUCES_POWERUP
		actualizarLuces(powerUp_cant,BACKGROUND)
		#VOLUMEN
		actualizarVolumen(volumen,BACKGROUND)

		##NOTAS EN PANTALLA
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
				nota.color= YELLOW
				nota.posx = POSINIYELLOW[0]
				nota.posy = POSINIYELLOW[1]
				notasSonando.append(nota)
			if notas[ritmo][3] == True:
				nota = disco_nota()
				nota.color= BLUE
				nota.posx = POSINIBLUE[0]
				nota.posy = POSINIBLUE[1]
				notasSonando.append(nota)
			if notas[ritmo][4] == True:
				nota = disco_nota()
				nota.color= ORANGE
				nota.posx = POSINIORANGE[0]
				nota.posy = POSINIORANGE[1]
				notasSonando.append(nota)
		ritmo+=1
		if ritmo == len(notas):
			ritmo = 0

		aEliminar=[]

		#LOGICA DE MOVIMIENTO y COLISION
		for nota in notasSonando:
			#muevo las notas la cantidad fija especificada..
			nota.posy += MOV_Y

			#chequeo colision..
			if notaActual[0]==True:
				pass
			if notaActual[1]==True:
				pass
			if notaActual[2]==True:
				pass
			if notaActual[3]==True:
				pass
			if notaActual[4]==True:
				pass


			if nota.posy >= 600:
				aEliminar.append(nota)
			pygame.draw.circle(BACKGROUND,nota.color, (nota.posx,nota.posy), 20, 0)

		


		##ELIMINAR NOTAS FUERA DE LA PANTALLA
		for nota in aEliminar:
			notasSonando.remove(nota)


		##DIBUJO LAS NOTAS QUE APRETA EL CLIENTE...
		if notaActual[0]==True:
			pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 0)
		if notaActual[1]==True:
			pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
		if notaActual[2]==True:
			pygame.draw.circle(BACKGROUND,YELLOW, (140,580), 20, 0)
		if notaActual[3]==True:
			pygame.draw.circle(BACKGROUND,BLUE, (200,580), 20, 0)
		if notaActual[4]==True:
			pygame.draw.circle(BACKGROUND,ORANGE, (260,580), 20, 0)
		
		
		##DIBUJO NOTAS APRETADAS DEL TECLADO
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key ==K_z:
					pygame.draw.circle(BACKGROUND,GREEN, (20,580), 20, 0)
					contador+=1
				if event.key==K_x:
					pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
					contador+=1
				if event.key == K_c:
					pygame.draw.circle(BACKGROUND,YELLOW,(140,580), 20, 0)
					contador+=1
				if event.key == K_v:
					pygame.draw.circle(BACKGROUND,BLUE, (200,580), 20, 0)
					contador+=1
				if event.key == K_b:
					pygame.draw.circle(BACKGROUND,ORANGE, (260,580), 20, 0)
					contador+=1
				
			elif event.type == QUIT:
#				print(contador)
				print('good bye')
				pygame.quit()
				sys.exit()

		##ACTUALIZO PANTALLA Y ESPERO AL SIGUIENTE TICK
		pygame.display.update()
		fpsClock.tick_busy_loop(FPS)	##siempre se llama luego del update()

##----------------------------FIN INICIAR_JUEGO()----------------------------------##



##EJEUTAMOS EN PARALELO SERVER Y EL JUEGO
#variables globales
notaActual =[False,False,False,False,False]

##-------HILOS---------
juegoH = threading.Thread(name='Juego', target=iniciar_juego)
serverH = threading.Thread(name='Server', target=iniciarServidor)

serverH.setDaemon(True)
juegoH.setDaemon(True)

serverH.start()
juegoH.start()

juegoH.join()
serverH.join()


