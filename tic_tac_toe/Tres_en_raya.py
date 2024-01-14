# coding: utf-8

# Vamos a crear el juego del 3 en raya

# Imports
import numpy as np
from random import randint

# Funciones
def cabecera():
	print('+---+---+---+')
	
def tablero(matriz):
    cabecera()
    for i in range(len(matriz)//3):
        print('| %s | %s | %s |' %(matriz[3*i], matriz[3*i + 1], matriz[3*i + 2]))
        cabecera()
	
def casillas_ganadoras(matriz,ficha):
    matriz = np.reshape(matriz,(3,3))
    ficha = np.asarray([ficha for i in range(len(matriz[:,0]))])
    anti_matriz = np.fliplr(matriz)
    
    if (np.diagonal(matriz) == ficha).all() or (np.diagonal(anti_matriz) == ficha).all():
        return True
    
    for i in range(len(matriz[:,0])):
        if (matriz[:,i] == ficha).all() or (matriz[i,:] == ficha).all():
            return True

def ganador(matriz,jugador,ficha):
    if casillas_ganadoras(matriz,ficha):
        print('El jugador %s gana' %jugador)
        return True
        
# Creemos el juego...
matriz = [' ' for i in range(1,9 + 1)] # Tablero

# Nick de los jugadores
jugador1 = input('Nombre jugador 1: ')
jugador2 = input('Nombre jugador 2: ')

print('El jugador %s juega con "O" y el jugador %s juega con "X"' %(jugador1,jugador2))

dicc = {jugador1 : 'O',jugador2 : 'X'}
jugadores = [jugador1,jugador2]

# Lanzamos una moneda para ver quién empieza
empieza = randint(0,1)
print('Comienza el jugador: ' + jugador1*(empieza == 0) + jugador2*(empieza == 1) + '\n')

# Jugada
for jugada in range(1,len(matriz) + 1):
    movimiento = int(input('Elige una casilla del 1 al 9: ')) - 1
    assert matriz[movimiento] == ' ',\
        'Solo puedes elegir casillas con un espacio en blanco'
	
    # Hacemos suma módulo 2 para obtener solo valores 0 o 1, en función del valor
    # de empieza y de la jugada tenemos un True o un False en dicc
    matriz[movimiento] = dicc[jugadores[((empieza + 1) % 2)*(jugada % 2 == 0) + empieza*(jugada % 2 != 0)]]
    print('Estado de la partida\n')
    tablero(matriz)
    
    # Comprobamos si hay ganador o tablas
    if ganador(matriz,jugador1,dicc[jugador1]): break
    elif ganador(matriz,jugador2,dicc[jugador2]): break
    elif jugada == 9:
        print('Partida en tablas')
        break
    
    print('\nTurno del jugador %s' %jugadores[((empieza + 1) % 2)*(jugada % 2 != 0) + empieza*(jugada % 2 == 0)])