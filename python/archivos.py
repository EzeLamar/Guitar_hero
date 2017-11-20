cancion=[]
acorde=[0,0,0]
CANT_NOTAS=3

with open("pepe.txt", "r") as fichero:
	for linea in fichero:
		notasLeidas=0
		leer_fila= linea.split(" ")
		while notasLeidas<CANT_NOTAS:
			acorde[notasLeidas]=leer_fila[notasLeidas]
			notasLeidas+=1
		cancion.append(acorde)
print(cancion)