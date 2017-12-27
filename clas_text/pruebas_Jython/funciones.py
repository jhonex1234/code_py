#funciones

#tupla prueba

tupa = (['jhon',12],['juan',13],['pedro',15])

def dic(tupaval):
    dc={}
    dt=0
    for d in range(0, len(tupaval)):
        dt=dt+1 
        dc[dt]=(tupa[d])
    return dc

val = dic(tupa)
print(val)
input(":)")


#funcion
def leer():
	for i in range(0,  len(tupa)):
	     print(tupa[i])
	     input("siguiente ->")

#leer()
