# A* Pathfinding Algorithm

## Descripción
Este proyecto implementa el algoritmo A* para encontrar el camino más corto entre un punto A y un punto B dentro de una cuadrícula configurable.

### Características:
- **Dimensión de la cuadrícula**: Permite establecer el tamaño de la cuadrícula.
- **Definir puntos A y B**: Selecciona el punto de inicio y el punto de destino.
- **Casillas bloqueadas**: Permite marcar obstáculos en la cuadrícula que no pueden ser atravesados.
- **Visualización del camino**: Muestra el camino óptimo calculado.

## Uso
1. Configura los parámetros:
   - Ingresa el tamaño de la cuadrícula.
   - Define la posición de los puntos A (inicio) y B (destino).
   - Agrega casillas bloqueadas según sea necesario.
2. Visualiza la solución generada por el algoritmo A*.

## Funcionamiento del Algoritmo A*
El algoritmo A* es una combinación de búsqueda en anchura (BFS) y búsqueda de costo uniforme (Dijkstra), utilizando la función heurística:

\[ f(n) = g(n) + h(n) \]

Donde:
- \( g(n) \) es el costo acumulado desde el punto de inicio hasta el nodo \( n \).
- \( h(n) \) es la estimación heurística de la distancia desde \( n \) hasta el punto B (utilizando la distancia Manhattan o Euclidiana).
- \( f(n) \) es la suma de ambas funciones para priorizar la expansión de los nodos más prometedores.

## Tecnologías utilizadas
- Python
- Algoritmo A*
- Biblioteca `pygame` (para visualización opcional)


