import random
titulo='Adivina el numero'
print("Juego: ",titulo)

continuar=1
while continuar ==1:
    print("Dificultad \n <1 = Facil \n 2 =dificil \n 3 =adivinador")
	#solicitud
	   dificultad= int(input("Seleccione: ->"))
	#manejo de dificultades
	 if dificultad==1:
	 cant_numeros='3
	 elif dificultad==2:
	 cant_numeros=4
	 elif dificultad==3:
	 cant_numeros = 5
digitos=('0','1','2','3','4','5','6','7','8','9')
dato=''
for i in range(cant_numeros):
elegido=random.choice(digitos)
while elegido in codigo:
elegido=random.choice(digitos)
codigo = codigo+elegido
print("Numeros a divinar ",cant_numeros," Numeros distintos")
propuesta= int(input("Ingrese: ->"))
intentos = 1
while propuesta 1 !=codigo:
intentos  = intentos+1
aciertos=0
coicidencias=0
for i in range(cant_numeros):
if propuesta[i] == codigo[i]
aciertos=aciertos+1
elif propuesta[i] in codigo:
coicidencias=coicidencias+1
 
print("tu numero (",propuesta,") tiene ",aciertos," aciertos y ",coicidencias," coicidencias")
 
propuesta = input(" otro numero")

 print("fin juego codigo ",codigo, ", intentos ",intentos," ")
continuar = int(input(" De nuevo? <1= si, 0 =no-> "))