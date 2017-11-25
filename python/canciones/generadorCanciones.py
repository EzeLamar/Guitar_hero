import pygame, sys
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

WHITE = (255,255,255)

pygame.mixer.init()
pygame.mixer.music.load(nameSong+'.mp3')
pygame.mixer.music.play(-1,0.0)

BACKGROUND = pygame.display.set_mode((400,600), 0, 32)

redApretado = False
greenApretado = False
blueApretado = False

FPS= 20 #FRAMES PER SECOND
fpsClock = pygame.time.Clock()
cancion = []
tempo = 0
grabar = True


while grabar:
	print(tempo)
	tempo+=1
#	BACKGROUND.fill(WHITE)
	acorde = 0

	greenApretado=False
	redApretado=False
	blueApretado=False
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key ==K_z:
				greenApretado= True
			if event.key==K_x:
				redApretado=True
			if event.key == K_c:
				blueApretado=True
			if event.key == K_q:
				pygame.mixer.music.stop()
				grabar=False
		if event.type == KEYUP:
			if event.key ==K_z:
				greenApretado= False
			if event.key==K_x:
				redApretado=False
			if event.key == K_c:
				blueApretado=False
	#determino el acorde segun botones apretados
	if greenApretado==True:
		acorde+=100
	if redApretado==True:
		acorde+=10
	if blueApretado==True:
		acorde+=1
	
	cancion.append(acorde)
	fpsClock.tick_busy_loop(FPS)
guardar_cancion(nameSong,cancion)
#print(cancion)
#pygame.mixer.music.stop()