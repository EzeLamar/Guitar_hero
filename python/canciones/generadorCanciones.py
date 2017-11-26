import pygame, sys, time
from pygame.locals import *

def guardar_cancion(nameSong,lista):
	f = open (nameSong+'.txt', 'w')
	for elemento in lista:
		f.write(str(elemento))
		f.write('\n')
	f.close()


pygame.init()

#solicita nombre de archivo a cargar:
nameSong = input("Ingrese nombre de cancion: ")
time.sleep(3)
WHITE = (255,255,255)

pygame.mixer.init()
pygame.mixer.music.load(nameSong+'.mp3')
pygame.mixer.music.play(-1,0.0)

BACKGROUND = pygame.display.set_mode((400,600), 0, 32)

redApretado = False
greenApretado = False
yellowApretado=False
blueApretado = False
orangeApretado=False

FPS= 20 #FRAMES PER SECOND
fpsClock = pygame.time.Clock()
cancion = []
tempo = 0
grabar = True


while grabar:
	print(tempo)
	tempo+=1
#	BACKGROUND.fill(WHITE)
	acorde = ""

	greenApretado=False
	redApretado=False
	blueApretado=False
	yellowApretado=False
	orangeApretado=False

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key ==K_z:
				greenApretado= True
			if event.key==K_x:
				redApretado=True
			if event.key == K_c:
				yellowApretado=True
			if event.key == K_v:
				blueApretado=True
			if event.key == K_b:
				orangeApretado=True
			

			if event.key == K_q:
				pygame.mixer.music.stop()
				grabar=False
		if event.type == KEYUP:
			if event.key ==K_z:
				greenApretado= False
			if event.key==K_x:
				redApretado=False
			if event.key == K_c:
				yellowApretado=False
			if event.key == K_v:
				blueApretado=False
			if event.key == K_b:
				orangeApretado=False
	#determino el acorde segun botones apretados
	if greenApretado==True:
		acorde= acorde+'1'
	else:
		acorde= acorde+'0'
	if redApretado==True:
		acorde= acorde+'1'
	else:
		acorde= acorde+'0'
	if yellowApretado==True:
		acorde= acorde+'1'
	else:
		acorde= acorde+'0'
	if blueApretado==True:
		acorde= acorde+'1'
	else:
		acorde= acorde+'0'
	if orangeApretado==True:
		acorde= acorde+'1'
	else:
		acorde= acorde+'0'

	cancion.append(acorde)
	fpsClock.tick_busy_loop(FPS)
guardar_cancion(nameSong,cancion)
#print(cancion)
#pygame.mixer.music.stop()