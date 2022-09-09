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

Ancho 10
Color de fondo Blanco

Avanzar Derecha Avanzar
Repetir 4 veces {
Repetir 8 veces { Pintar Negro Avanzar }
Derecha Derecha Avanzar Derecha
}

Repetir [1-9]+ veces \{[ |\n][Izquierda|Derecha|Avanzar ]

Izquierda|Derecha|Avanzar [0-9\n]*|Repetir [0-9] veces|Pintar (Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\))|Repetir [0-9] veces
'''

matrix_completa=r"(Ancho (?P<area>[0-9]+)) (Color de fondo (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))"
patinstru=r"(Izquierda|Derecha|Avanzar ?(?P<avance>[0-9\n])*|(?P<pintar>Pintar (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))|(?P<repetir>Repetir (?P<numero>[0-9]*) veces \{(?P<contllave>[^}]*)}))"
repetir=r"(Repetir (?P<numero>[0-9]*) veces \{(?P<contllave>[^}]*)})"
pintcolor=r"(?P<pintar>Pintar (?P<color>Rojo|Verde|Azul|Negro|Blanco|RGB\([0-9]{1,3}\,[0-9]{1,3},[0-9]{1,3}\)))"





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

'''
Funcion 'convertirargb'
    parametros:
            rgb (str): nombre del color o codigo rgb encontrado por la expresion regular
    retorno:
            evalr(rgb): retorna una tupla de enteros, esto con el fin de poder utilizar la funcion 'MatrizImagen'correctamente
'''

def crearmatriz(matsize,color):
    cod=convertirargb(color)
    num=int(matsize)
    matriz=[]
    for i in range(num):
        matriz.append([cod]*num)
    return matriz

'''
Funcion 'crearmatriz'
    parametros:
            matzise (str): tamaño de la matriz (N x N) en forma de string, se obtiene luego de aplicar la expresion regular al comando 'pintar'
            color (str): nombre del color o codigo rgb encontrado por la expresion regular 
    retorno:
            matriz (list): lista de listas compuestas por 3-tupla con su codigo RGB correspondiente y del tamaño obtenido por las instrucciones 
'''

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
'''
Funcion 'girar'
    parametros:
            direccion (str): Puede ser Derecha o Izquierda y sirve para poder realizar un giro de 90 grados en la direccion obtenida
            apuntando (int): numero de la posicion actual donde:
                        #arriba=0 disminuye x
                        #derecha=1 aumenta y
                        #abajo=2 aumenta x
                        #izquierda=3 disminuye y
    retorno:
            pos (int): numero correspondiente a la posicion en la que se esta apuntando para un futuro avance:
                        #arriba=0 disminuye x
                        #derecha=1 aumenta y
                        #abajo=2 aumenta x
                        #izquierda=3 disminuye y
'''

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


test=open("codigo.txt","r")


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
'''
La parte de codigo anterior crea dos variables que contienen strings, defmatrix contiene las especificaciones de la matriz (color, tamaño)
e instrucciones contiene todas las instrucciones necesarias para crear el pixelart 
'''
compileforma=re.match(matrix_completa,formato)
size=compileforma.group('area')
matcolor=compileforma.group('color')
matrix=crearmatriz(size,matcolor)
posx=0
posy=0
pointing=1
posactual= matrix[posx][posy]
reinstru=re.findall(patinstru,instrucciones)

'''
En la parte anterior del codigo se obtienen los datos necesarios para formar la matriz inicial con el correspondiente tamaño y color de fondo.
Tambien se agregan los valores iniciales necesarios para realizar los cambios en la matriz.
'''



cmp1=instrucciones
cmp2=""
res=""
for a in reinstru:
    cmp2+=a[0]+" "
cmp1+=" "
cmp2=cmp2.replace("  "," ")
if len(cmp1)>len(cmp2):
    res=cmp1.replace(cmp2,'')
else: 
    res=cmp2.replace(cmp1,'')

if res !="":
    errores=open("errores.txt","w")
    errores.write(res)
    errores.close()
    sys.exit()
test.close()

'''
La parte de codigo anterior corresponde a la verificacion de errores, funciona comparando los matches de la expresion regular con el texto de instrucciones, 
si existen diferencias, estas seran agregadas a un txt como los errores de sintaxis
'''

def general(txt,reps):
    global pointing
    global posx
    global posy
    reinstru=txt
    while reps > 0:
        for a in reinstru:
            if a[0] == "Izquierda" or a[0] == "Derecha":
                pointing= girar(a[0],pointing)
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
                match=re.match(repetir,a[0])
                repets=int(match.group("numero"))
                texto=match.group("contllave")
                texto2=re.findall(patinstru,texto)
                general(texto2,repets)
        reps-=1
    return

'''
Funcion 'general'
    parametros:
            txt (str): cadena de texto con instrucciones, esta sera utilizada para obtener las instrucciones de dibujo del pixelart
            reps (int): cantidad de veces la que se repetira el analisis del parametro txt, su primer uso debe ser 1. Su uso es para poder 
                        aplicar el comando repetir una x cantidad de veces
    retorno:
            return vacio es utilizado para poder aplicar la recursividad
'''


general(reinstru,1)
MatrizAImagen(matrix)
