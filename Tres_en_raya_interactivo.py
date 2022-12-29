# coding: utf-8

'''
Formato del tablero:

+----+----+----+
| 11 | 12 | 13 |
+----+----+----+
| 21 | 22 | 23 |
+----+----+----+
| 31 | 32 | 33 |
+----+----+----+
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Funciones
def tablero(fig,L):
    tabx = np.linspace(0,L,4)
    taby = tabx*1.
    X,Y = np.meshgrid(tabx,taby)

    fig.plot(X,Y,'k-')
    fig.plot(Y,X,'k-')
    fig.axis('equal')
	
def aspas(fig,L,jugador,posx = 0,posy = 0):
    x = np.arange(-1,2)*L/12.
    y = np.arange(-1,2)*L/12.
    
    fig.plot(x + posx,y + posy,'r-')
    fig.plot(-x + posx,y + posy,'r-')
    fig.axis('equal')
    plt.title(u'Turno del jugador ' + jugador,fontsize = 'x-large')
    plt.draw()
	
def circulo(fig,L,jugador,posx = 0,posy = 0):
    R = 1.5*L/12
    theta = np.arange(0,2*np.pi,0.0001)
    
    fig.plot(R*np.cos(theta) + posx,R*np.sin(theta) + posy,'b-')
    fig.axis('equal')
    plt.title(u'Turno del jugador ' + jugador,fontsize = 'x-large')
    plt.draw()

def cuadrante(coord,L):
    x = coord[0,0]
    y = coord[0,1]
    
    Lvec = np.array([0,L/3.,2*L/3.,L])
    
    ix1 = np.max(np.where(Lvec <= x))
    ix2 = np.min(np.where(Lvec >= x)) # Una vez tenemos ix1, ix2 = ix1 + 1
    
    iy1 = np.max(np.where(Lvec <= y))
    iy2 = np.min(np.where(Lvec >= y))
    
    return ix1,ix2,iy1,iy2,Lvec

def poner_ficha(coord,L,jugada,empieza,jugadores,dicc,matriz):
    ix1,ix2,iy1,iy2,Lvec = cuadrante(coord,L)
    player = jugadores[((empieza + 1) % 2)*(jugada % 2 != 0) + empieza*(jugada % 2 == 0)]
    
    if (jugada % 2 == 0 and empieza == 0) or (jugada % 2 != 0 and empieza == 1):
        assert type(matriz[ix1][iy1]) !=  str,\
        'Solo puedes elegir casillas con un espacio en blanco'
        matriz[ix1][iy1] = dicc[jugadores[1]] # En el if hemos eliminado el caso de círculo
        aspas(ax,L,player,posx = (Lvec[ix1] + Lvec[ix2])/2.,posy = (Lvec[iy1] + Lvec[iy2])/2.)
        
    elif (jugada % 2 == 0 and empieza == 1) or (jugada % 2 != 0 and empieza == 0):
        assert type(matriz[ix1][iy1]) !=  str,\
        'Solo puedes elegir casillas con un espacio en blanco'
        matriz[ix1][iy1] = dicc[jugadores[0]]
        circulo(ax,L,player,posx = (Lvec[ix1] + Lvec[ix2])/2.,posy = (Lvec[iy1] + Lvec[iy2])/2.)
        
def casillas_ganadoras(matriz,ficha):
    matriz = np.asarray(matriz)
    matriz[[0,-1]] = matriz[[-1,0]] # Para revisar si hay ganador hay que intercambiar
                                    # la primera con la última fila pues asignamos que
                                    # la parte de abajo del tablero fuera la primera 
                                    # fila de la matriz
    ficha = np.asarray([ficha for i in range(len(matriz[:,0]))])
    anti_matriz = np.fliplr(matriz)
    
    if (np.diagonal(matriz) == ficha).all() or (np.diagonal(anti_matriz) == ficha).all():
        return True
    
    for i in range(len(matriz[:,0])):
        if (matriz[:,i] == ficha).all() or (matriz[i,:] == ficha).all():
            return True

def ganador(matriz,jugador,ficha):
    if casillas_ganadoras(matriz,ficha):
        plt.title(u'El jugador ' + jugador + ' gana',fontsize = 'x-large')
        return True
    
# Longitud del tablero
L = 12

# Nicks de los jugadores
jugador1 = input(u'Nombre jugador 1: ')
jugador2 = input(u'Nombre jugador 2: ')

print('El jugador %s juega con "O" y el jugador %s juega con "X"' %(jugador1,jugador2))

dicc = {jugador1 : 'O',jugador2 : 'X'}
jugadores = [jugador1,jugador2]

# Lanzamos una moneda para ver quién empieza
empieza = np.random.randint(0,2)
print('Comienza el jugador: ' + jugador1*(empieza == 0) + jugador2*(empieza == 1) + '\n')

# Creamos el tablero de texto
matriz = [[0,0,0] for i in range(3)]

# Creamos el tablero interactivo
fig = plt.figure(figsize = (5,5))
ax = fig.add_subplot(111)

tablero(ax,L)
plt.title(u'Turno del jugador ' + jugador1*(empieza == 0) + jugador2*(empieza == 1),fontsize = 'x-large')

# Inicializamos la jugada
jugada = 1
while True:
    coord = fig.ginput() # Coordenadas del click
    coord = np.asarray(coord)
    
    player = jugadores[((empieza + 1) % 2)*(jugada % 2 != 0) + empieza*(jugada % 2 == 0)]
    plt.title(u'Turno del jugador ' + player)
    plt.draw()

    poner_ficha(coord,L,jugada,empieza,jugadores,dicc,matriz)
    
    # Comprobamos si hay ganador o tablas
    if ganador(matriz,jugador1,dicc[jugador1]): break
    elif ganador(matriz,jugador2,dicc[jugador2]): break
    
    jugada += 1
    if jugada == 10:
        plt.title(u'Tablas',fontsize = 'x-large')
        break
    
plt.show()
