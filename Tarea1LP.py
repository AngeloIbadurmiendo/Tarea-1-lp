import re
import numpy as np 
from PIL import Image 
import sys
'''

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
        codigo=(255,0,0)
    elif input == 'verde':
        codigo=(0,255,0)
    elif input == 'azul':
        codigo=(0,0,255)
    elif input == 'negro':
        codigo=(0,0,0)
    elif input == 'blanco':
        codigo=(255,255,255)
    else:
        rgb=colname[3:]
        return eval(rgb)
    return codigo

def crearmatriz(matsize,color):
    cod=convertirargb(color)
    num=int(matsize)
    matriz=[]
    for i in range(num):
        matriz.append([cod]*num)
    return matriz

def girar(direccion,apuntando):
    direccion=direccion.lower()
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

def MatrizAImagen(matriz, filename='pixelart.png', factor=10):
    '''
    Convierte una matriz de valores RGB en una imagen y la guarda como un archivo png.
    Las imagenes son escaladas por un factor ya que con los ejemplos se producirian imagenes muy pequeñas.
        Parametros:
                matriz (lista de lista de tuplas de enteros): Matriz que representa la imagen en rgb.
                filename (str): Nombre del archivo en que se guardara la imagen.
                factor (int): Factor por el cual se escala el tamaño de las imagenes.
    '''
    matriz = np.array(matriz, dtype=np.uint8)
    np.swapaxes(matriz, 0, -1)

    N = np.shape(matriz)[0]

    img = Image.fromarray(matriz, 'RGB')
    img = img.resize((N*10, N*10), Image.Resampling.BOX)
    img.save(filename)

matrix_completa=r"(Ancho (?P<area>[0-9]+)) (Color de fondo (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))"
patinstru=r"(Izquierda|Derecha|Avanzar ?(?P<avance>[0-9\n])*|(?P<pintar>Pintar (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))|(?P<repetir>Repetir (?P<numero>[0-9]*) veces \{[^}]*}))"
pintcolor=r"(?P<pintar>Pintar (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))"

#arriba=0 disminuye x
#derecha=1 aumenta y
#abajo=2 aumenta x
#izquierda=3 disminuye y
#mirando hacia la derecha
# 0 y 2 movimiento en x
# 1 y 3 movimiento en y
#para avanzar usar la condicion de movimiento en x o y (if pointing == 0 o 2 sumar/restar la cantidad a 'X' 1 o 3 sumar/restar la cantidad a 'Y')

test=open("tests.txt","r")
defmatrix=[]
instrumatrix=[]

for a in test:
    defmatrix.append(a)
    instrumatrix.append(a)
defmatrix= defmatrix[0:2]
instrumatrix=instrumatrix[3:]
defmatrix=[w.replace("\n"," ") for w in defmatrix]
instrumatrix=[w.replace("\n"," ") for w in instrumatrix]
formato=""
instrucciones=""
for a in defmatrix:
    formato+=a
for a in instrumatrix:
    instrucciones+=a

compileforma=re.match(matrix_completa,formato)
size=compileforma.group('area')
matcolor=compileforma.group('color')
matrix=crearmatriz(size,matcolor)
posx=0
posy=0
pointing=1
posactual= matrix[posx][posy]
reinstru=re.findall(patinstru,instrucciones)
errores=""
cmp1=instrucciones
cmp2=""
res=""
for a in reinstru:
    cmp2+=a[0]
if len(cmp1)>len(cmp2): 
    res=cmp1.replace(cmp2,'')
else: 
    res=cmp2.replace(cmp1,'')
print (res)


for a in reinstru:
    if a[0] == "Izquierda" or a[0] == "Derecha":
        pointing=girar(a[0],pointing)
    elif 'Avanzar' in a[0] and "Repetir" not in a[0]:
        num=a[0][-1]
        if num==" ":
            num=1
        num=int(num)
        if pointing==0:
            posx-=num
            if posx<0:
                print("Fuera de los limites")
                sys.exit()
        elif pointing ==1:
            posy+=num
            if posy>(int(size)-1):
                print("fuera de los limites")
                sys.exit()
        elif pointing == 2:
            posx+=num
            if posx>(int(size)-1):
                print("fuera de los limites")
                sys.exit()
        elif pointing == 3:
            posy-=num
            if posy<0:
                print("fuera de los limites")
                sys.exit()
    elif "Pintar" in a[0] and "Repetir" not in a[0]:
        match=re.match(pintcolor,a[0])
        color=convertirargb(match.group("color"))
        matrix[posx][posy]=color
    elif "Repetir" in a[0]:
        print("\n")
    
    
        




