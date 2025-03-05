Actividad 1 REDES NEURONALES

# Modelar una red neuronal que pueda jugar al 5 en linea sin gravead en un tablero de 20x20
# 1.-Definir el tipo de red neuronal y describir cada una de sus partes.
    Red convulcional, Red Profunda.
    
    La uso porque se que puede manejar mas de 2 variables.

    Mis entradas serian:
     0 = Ficha vacia
     1 = Ficha propia
    -1 = Ficha enemiga

    Mis capas serian 3 
    1.- si hay filas de 2,3 o 4 para lineas que pueden ser las ganadoras
    2.- bloqueos , estos son para bloquear que el jugador contrario gane
    3.- espacios vacios, para ver cuales son los espacios vacion restantes para poder formar la estrategia

    Mi salida seria una capa densa
    Ya que como tengo que estar evaluando el table de 20x20 necesito poder abarcar las 400 celdas para poder tener la informacion necesaria para determinar mis movimientos. Por lo tanto mi capa densa deberia tener almenos 400 neuronas, una para cada celda.


# 2.- Definir los patrones a utilizar.

    Un jugador normal debe considerar el evitar que bloqueen sus lineas, 
    ver los espacion libres para poder formar lineas ganadoras, 
    evitar que el jugador gane bloqueando sus posibles lineas ganadoras y evitar los bordes del mapa, ya que estos limitan las posibilidades de formar un alinea

# 3.- Definir la funcino de activacion necesaria para este problema.

    El empezar por los turnos correspondientes, si tengo el turno inicial, elegir la psocion mas ventajosa al inicio de la partida que seria el centro

    En el caso contrario de que empiece el contrario, elegir una posicion ventajosa y/o que pueda bloquear la linea del enemigo.

# 4.- Definir el numero maximo de entradas.

    Ficha vacia, Ficha enemiga, Ficha propia

# ¿que valores ,a la salida de la red, se podrian esperar?

    Ya que el tablero se puede representar como una matriz de 20x20, cada celda puede tener un valor cercano al -1, 0 o 1, ya que estos son los que representan si una celda esta vacia o ocupada por alguno de los dos jugadores.

    Estos los podemos interpretar como:
    Valores cercanos a 1 = Posciciones o movimientos que nos benefician como jugador
    Valores cercanos a 0 = Movimientos que no generarian gran impacto en la jugada
    Valores cercanos a -1 = Movimientos que benefician al contrario     

# ¿Cuales valores son valores maximos que puede tener el bias?

