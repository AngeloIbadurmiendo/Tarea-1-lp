import numpy as np

'''regex
matsize="[A|a]ncho (?P<area>[0-9]+)"
color="([C|c]olor de fondo (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))"


def convertirargb(colname):
    input=colname.lower()
    codigo=''
    if input == 'rojo':
        codigo='(255,0,0)'
    if input == 'verde':
        codigo='(0,255,0)'
    if input == 'azul':
        codigo='(0,0,255)'
    if input == 'negro':
        codigo='(0,0,0)'
    if input == 'blanco':
        codigo='(255,255,255)'
    return codigo

listacolores=['rojo','verde','azul','negro','blanco']
if colorentregado(no codigo) in listacolores:
    convertirargb(colorentregado)





ejemplos
Avanzar Derecha Avanzar
Repetir 4 veces {
Repetir 8 veces { Pintar Negro Avanzar } 
Derecha Derecha Avanzar Derecha }
Pintar Rojo Avanzar 2 Derecha
Pintar Verde Avanzar 2 Derecha
Pintar Azul Avanzar 2 Derecha
Pintar Blanco Avanzar Derecha Avanzar
Pintar RGB(0,255,255)



Repetir [1-9]+ veces \{[ |\n][Izquierda|Derecha|Avanzar ]

Izquierda|Derecha|Avanzar [0-9\n]*|Repetir [0-9] veces|Pintar (Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\))|Repetir [0-9] veces
'''


def convertirargb(colname):
    input=colname.lower()
    codigo=''
    if input == 'rojo':
        codigo='(255,0,0)'
    elif input == 'verde':
        codigo='(0,255,0)'
    elif input == 'azul':
        codigo='(0,0,255)'
    elif input == 'negro':
        codigo='(0,0,0)'
    elif input == 'blanco':
        codigo='(255,255,255)'
    else:
        return colname
    return codigo


def crearmatriz(matsize,color):
    cod=convertirargb(color)
    matriz=[]
    for i in range(matsize):
        matriz.append([cod]*matsize)
    return matriz

def girar(direccion,apuntando):
    pos=apuntando
    if direccion=='derecha':
        if pos>=3:
            pos=-1
        pos+=1
    if direccion=='izquierda':
        if pos<=0:
            pos=4
        pos-=1
    return pos

size=3
color='(255,30,20)'
#matrix=crearmatriz(size,color)
matrix=[['00', '01', '02'], ['10', '11', '12'], ['20', '21', '22']]
'''
[['00', '01', '02'],
 ['10', '11', '12'], 
 ['20', '21', '22']]'''
#arriba=0 disminuye x
#derecha=1 aumenta y
#abajo=2 aumenta x
#izquierda=3 disminuye y
#mirando hacia la derecha
# 0 y 2 movimiento en x
# 1 y 3 movimiento en y
#para avanzar usar la condicion de movimiento en x o y (if pointing == 0 o 2 sumar/restar la cantidad a 'X' 1 o 3 sumar/restar la cantidad a 'Y')
posx=0
posy=0
pointing=1
posactual= matrix[posx][posy]

print("hola")







    


    


    




