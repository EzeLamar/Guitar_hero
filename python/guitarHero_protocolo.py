##FALTA:
	#VICTORIA/DERROTA:
		#Derrota:
			#si se erra una cant de notas fija, ent automaticamente se pierde
			#enviar msje  que indique derrota.
		#Victoria:
			#cuando termina la cancion si no se perdió se detiene el juego
			#enviar un msje que indice victoria.
		#LUCES:
			#ver por que no se apagan las luces al consumirlas el poder.

##ESTADO_PARTIDA:
#estado_partida=0 -> no comenzo la partida
#estado_partida=1 -> comenzo la partida
#estado_partida=2 -> se gano la partida
#estado_partida=3 -> se perdio la partida

import pygame, sys, os, time, threading, socket, errno
from socket import error as SocketError
from pygame.locals import *


def actualizarVolumen(cantVol, BACKGROUND):
	BLACK= (0,0,0)
	WHITE= (255,255,255)
	X_INICIAL=330 
	Y_INICIAL=200

	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 28)
	textSurfacePuntaje = textoPuntajeObj.render("vol:"+str(int(pygame.mixer.music.get_volume()*100))+"%", True, BLACK, WHITE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	##con esto actualizo
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)

def actualizarMultiplicador(valor, BACKGROUND):
	BLACK= (0,0,0)
	WHITE= (255,255,255)
	X_INICIAL=380 
	Y_INICIAL=580
	
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 32)
	textSurfacePuntaje = textoPuntajeObj.render("x"+str(valor), True, BLACK, WHITE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	##con esto actualizo
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)


def cartel_victoria(BACKGROUND):
	WHITE= (255,255,255)
	GOLD= (255,215,0)
	X_INICIAL=200 
	Y_INICIAL=300
	
	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 60)
	textSurfacePuntaje = textoPuntajeObj.render(("YOU ROCK!"), True, WHITE, GOLD)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	##con esto actualizo
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)


def cartel_derrota(BACKGROUND):
	RED= (255,0,0)
	BLACK= (0,0,0)
	X_INICIAL=200 
	Y_INICIAL=300
	
	sonido=pygame.mixer.Sound('Abucheo.wav')
	sonido.play()

	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 60)
	textSurfacePuntaje = textoPuntajeObj.render(("YOU SUCK!"), True, RED, BLACK)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	##con esto actualizo
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)
	time.sleep(3)


def actualizarAciertos(cantAcertadas,cantErradas, BACKGROUND):
	BLACK= (0,0,0)
	WHITE= (255,255,255)
	X_INICIAL=300 
	Y_INICIAL=400

	textoPuntajeObj = pygame.font.Font('freesansbold.ttf', 20)
	#escribo aciertos:
	textSurfacePuntaje = textoPuntajeObj.render("ac:"+str(cantAcertadas), True, BLACK, WHITE)
	textRectPuntaje = textSurfacePuntaje.get_rect()
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL)
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)
	##escribo errores:
	textSurfacePuntaje = textoPuntajeObj.render("err:"+str(cantErradas), True, BLACK, WHITE)
	textRectPuntaje.center = (X_INICIAL,Y_INICIAL+100)
	BACKGROUND.blit(textSurfacePuntaje, textRectPuntaje)



def actualizarLuces(cantEncendidas, CELESTE,BACKGROUND):
	CELESTE= (0,191,255)
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
			pygame.draw.circle(BACKGROUND,CELESTE, (pos_x,Y_INICIAL) , RADIO, 0)
		else:
			pygame.draw.circle(BACKGROUND,CELESTE, (pos_x,Y_INICIAL) , RADIO, 4)

##----------------SERVIDOR TCP-----------------------




def iniciarServidor():
	#variable global compartida
	global notaActual
	global volumen
	global powerUp_activado
	global powerUp_cant
	global multiplicador
	global estado_partida

	#CONSTANTES
	COMIENZO_CARACT=63

	#LOCALES
	multiplicadorActual=multiplicador
	powerUp_cantActual=powerUp_cant
	jugando=True

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = ('192.168.0.4', 8888)
	print('starting up on port',server_address)
	sock.bind(server_address)

	# Listen for incoming connections
	sock.listen(2)
	while jugando:
		# Wait for a connection
		print('waiting for a connection')
		connection, client_address = sock.accept()
		try:
			print('connection from', client_address)
			# Receive the data in small chunks and retransmit it
			while jugando:
				time.sleep(0.01)
#				time.sleep(0.1)
				
				##VERIFICO QUE TIPO DE PAQUETE ENVIAR
				#VICTORIA/DERROTA
				if estado_partida==2:	#verifico si GANO
					victoria_msje="<7$5$1>"
					connection.sendall(victoria_msje.encode("utf-8"))
					jugando=False
					break

				elif estado_partida==3:
					derrota_msje="<7$5$0>"
					connection.sendall(derrota_msje.encode("utf-8"))
					jugando=False
					break

				#en caso que el multiplicador cambie..
				elif multiplicador!=multiplicadorActual:
					multiplicadorActual=multiplicador
					multiplicador_msje="<7$6$"+str(multiplicadorActual)+">"
					connection.sendall(multiplicador_msje.encode("utf-8"))
				#en caso que el powerUp_cant cambie..
				elif powerUp_cantActual!=powerUp_cant:
					powerUp_cantActual=powerUp_cant	
					PUcant_msje= "<7$4$"+str(powerUp_cantActual)+">"
					connection.sendall(PUcant_msje.encode("utf-8"))

				##PAQUETE REFRESCO
				else:		
					refresco_msje="<6$3$>"
					#envio el paquete REFRESCO
					connection.sendall(refresco_msje.encode("utf-8"))
#					print('waiting next package from client')
					#recibo la respuesta del Cliente
					msje= connection.recv(7).decode("utf-8") 
#					print('received ', msje)
					if msje:
						##DIVIDO EL MSJE SEGUN LOS SEPARADORES '$'
						camposMsje= msje.split('$')
#						print("paquete ",camposMsje)
						##OBTENGO CAMPO TIPO:
						campoTipo=camposMsje[1]
						##SEGUN EL TIPO OBTENEMOS (O NO) EL PAYLOAD
						#si el tipo es '0' (TECLAS):
						if campoTipo=='0':
							campoPayload= camposMsje[2][:-1]
	#						print('es de tipo 0..')
#							print(campoPayload)
							#obtenemos la nota correspondiente:
							nroPayload= ord(campoPayload)-COMIENZO_CARACT
#							print("el # de nota es: ", nroPayload)
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
							#chequeo si ya estaba hablitado y cuantas luces hay encendidas
							if powerUp_activado==False and powerUp_cant>=2:
								powerUp_activado=True

						elif campoTipo=='2':
	#						print('es de tipo 2..')
							#obtenemos el volumen correspondiente:
							campoPayload= camposMsje[2][:-1]
							volumen= int(campoPayload)
					else:
						print('no more data from ', client_address)
						break
		except SocketError as e:
			if e.errno != errno.ECONNRESET:
				pass
			pass
		finally:
			# Clean up the connection
			connection.close()


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

			#determino que acorde es:
			NroAcorde= linea
			acorde=convertirAcordeBinario(NroAcorde)
			cancion.append(acorde)
	return cancion


class disco_nota:
	color= (0,0,0)
	posx = 0
	posy = 0
	altura= 40

def iniciar_juego():
	##VARIABLES GLOBAlES
	global notaActual
	global volumen
	global powerUp_activado
	global powerUp_cant
	global multiplicador
	global estado_partida
	estado_partida=1 	#comenzo la partida

	#CONSTANTES
	CANT_MAX_ERRADAS= 200	#si se erran esta cant el jugador pierde la partida
	N_RITMOS = 18
	TIEMPO_POWERUP_POR_LUZ=5

	##locales
	
	cantAcertadas=0
	cantErradas =0
	cantSeguidas=0
	volumenActual=volumen
	contadorTicksPU=0


	pygame.init()

	
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

	CELESTE= (0,191,255)
	GREY =(128,128,128)

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

	##MUSICA DE FONDO
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


	while estado_partida==1:
#		print(estado_partida)
#		print(ritmo)
		
		#arranco la musica luego de N ritmos
		if ritmo==N_RITMOS and not musicaReproduciendo:
			print('comienza la musica!')
			pygame.mixer.music.set_volume(1.0)
			pygame.mixer.music.play(0,0.0)
			musicaReproduciendo= True

		##--------------------GUI----------------------------
		#VENTANA
		#si el poder esta activaso el fondo se pone GREY
		if powerUp_activado:
			BACKGROUND.fill(GREY)
		#caso contrario el fondo es WHITE
		else:
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
		actualizarLuces(powerUp_cant,CELESTE, BACKGROUND)

		#VOLUMEN
		actualizarVolumen(volumen,BACKGROUND)
		if volumenActual!=volumen:
			volumenActual=volumen
			#valor entre 0-4
			#0 -> 0.0	|	1 -> 0.25	|	2 -> 0.5	|	3 -> 0.75	|	4 -> 1.0
			pygame.mixer.music.set_volume(volumenActual*0.25)

		#ACIERTOS
		actualizarAciertos(cantAcertadas,cantErradas,BACKGROUND)
		#MULTIPLICADOR
		actualizarMultiplicador(multiplicador,BACKGROUND)
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

		##LOGICA DE MOVIMIENTO y COLISION
		aEliminar=[]
		seApreto=False
		for nota in notasSonando:
			#muevo las notas la cantidad fija especificada..
			nota.posy += MOV_Y
			
			#chequeo si hay una nota en el espacio de la nota verde
			if nota.color==GREEN and notaActual[0]==True:
					if abs(560-nota.posy)<40:
						seApreto=True
			elif nota.color==RED and notaActual[1]==True:
					if abs(560-nota.posy)<40:
						seApreto=True
			elif nota.color==YELLOW and notaActual[2]==True :
					if abs(560-nota.posy)<40:
						seApreto=True
			elif nota.color==BLUE and notaActual[3]==True:
					if abs(560-nota.posy)<40:
						seApreto=True
			elif nota.color==ORANGE and notaActual[4]==True:
					if abs(560-nota.posy)<40:

						seApreto=True

			if seApreto==True:
				aEliminar.append(nota)
				#luces PowerUP
				if powerUp_activado==False:
					if cantAcertadas%30==0:
						powerUp_cant+=1
						if powerUp_cant>4:
							powerUp_cant=4
				#multiplicador
				cantSeguidas+=1
				cantAcertadas+=1
				seApreto=False
			elif nota.posy > 600:
				aEliminar.append(nota)
				cantErradas+=1
				#multiplicador
				cantSeguidas=0

			##DIBUJO LAS NOTAS EN PANTALLA
			#dibujo todas las notas CELESTES si el powerUp esta habilitado
			if powerUp_activado:
				pygame.draw.circle(BACKGROUND,CELESTE, (nota.posx,nota.posy), 20, 0)
			#caso contrario dibujo las notas con su color correspondiente
			else:
				pygame.draw.circle(BACKGROUND,nota.color, (nota.posx,nota.posy), 20, 0)

		

		##ELIMINAR NOTAS FUERA DE LA PANTALLA
		for nota in aEliminar:
			notasSonando.remove(nota)

		##ACTUALIZO MULTIPLICADOR
		#---------normal--------|-powerUp-
		#10 notas seguidas ->x2 |-> x4
		#20 notas seguidas ->x3 |-> x6
		#30 notas seguidas ->x4 |-> x8
		if powerUp_activado:
			if cantSeguidas<10:
				multiplicador=2
			elif cantSeguidas<20:
				multiplicador=4
			elif cantSeguidas<30:
				multiplicador=6
			elif cantSeguidas>=30:
				multiplicador=8
		else:	
			if cantSeguidas<10:
				multiplicador=1
			elif cantSeguidas<20:
				multiplicador=2
			elif cantSeguidas<30:
				multiplicador=3
			elif cantSeguidas>=30:
				multiplicador=4

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
					notaActual=[True,True,True,True,True]
					contador+=1
				if event.key==K_x:
					pygame.draw.circle(BACKGROUND,RED, (80,580), 20, 0)
					powerUp_cant=0
					contador+=1
				if event.key == K_c:
					pygame.draw.circle(BACKGROUND,YELLOW,(140,580), 20, 0)
					contador+=1
				if event.key == K_v:
					contador+=1
				if event.key == K_b:
					pygame.draw.circle(BACKGROUND,ORANGE, (260,580), 20, 0)
					notaActual=[False,False,False,False,False]
					contador+=1
				
			elif event.type == QUIT:
				estado_partida=0
				print('good bye')
				pygame.quit()
				time.sleep(3)
				sys.exit()
		
		##LOGICA LUCES POWERUP
		if powerUp_activado==True:
			if powerUp_cant>0:
				if contadorTicksPU<FPS*TIEMPO_POWERUP_POR_LUZ:
					contadorTicksPU+=1
				else:
					contadorTicksPU=0
					powerUp_cant-=1
			else:
				powerUp_activado=False

		##LOGICA DE VICTORIA/DERROTA
		#DERROTA: comparo si la cant de notas erradas es el maximo
		if cantErradas>=CANT_MAX_ERRADAS:
			estado_partida=3	#estado de derrota
			pygame.mixer.music.stop()
			cartel_derrota(BACKGROUND)
		elif musicaReproduciendo and  pygame.mixer.music.get_busy()==False:
			estado_partida=2	#estado de victoria
			cartel_victoria(BACKGROUND)


		##ACTUALIZO PANTALLA Y ESPERO AL SIGUIENTE TICK
		pygame.display.update()
		fpsClock.tick_busy_loop(FPS)	##siempre se llama luego del update()

##----------------------------FIN INICIAR_JUEGO()----------------------------------##



##EJEUTAMOS EN PARALELO SERVER Y EL JUEGO
#variables globales
notaActual =[False,False,False,False,False]
powerUp_activado=False
powerUp_cant=0
volumen=4
multiplicador=1
estado_partida=0	




##-------HILOS---------
juegoH = threading.Thread(name='Juego', target=iniciar_juego)
serverH = threading.Thread(name='Server', target=iniciarServidor)

serverH.setDaemon(True)
juegoH.setDaemon(True)

serverH.start()
juegoH.start()

juegoH.join()
serverH.join()


