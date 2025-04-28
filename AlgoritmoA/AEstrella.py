import pygame
import heapq

pygame.init()

# Configuración de la ventana
ANCHO_VENTANA = 700
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización A* con Costos y Animación")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

# Fuente
FUENTE = pygame.font.SysFont('consolas', 12)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas

        self.g = float("inf")
        self.h = 0
        self.f = 0
        self.vecinos = []

    def __eq__(self, other):
        return isinstance(other, Nodo) and self.fila == other.fila and self.col == other.col

    def __hash__(self):
        return hash((self.fila, self.col))

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = 0
        self.f = 0

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        if self.color not in (NARANJA, PURPURA):
            self.color = VERDE

    def hacer_abierto(self):
        if self.color not in (NARANJA, PURPURA):
            self.color = GRIS_CLARO

    def dibujar(self, ventana, fuente):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.f != 0 and self.f != float("inf"):
            h_texto = fuente.render(f"h:{int(self.h)}", True, NEGRO)
            f_texto = fuente.render(f"f:{int(self.f)}", True, NEGRO)
            g_texto = fuente.render(f"g:{int(self.g)}", True, NEGRO)
            ventana.blit(f_texto, (self.x + 1, self.y + 1))
            ventana.blit(g_texto, (self.x + 1, self.y + self.ancho // 2 - 8))
            ventana.blit(h_texto, (self.x + 1, self.y + self.ancho - 16))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        direcciones = [
            (1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10),
            (1, 1, 14), (1, -1, 14), (-1, 1, 14), (-1, -1, 14)
        ]
        for df, dc, costo in direcciones:
            nueva_fila = self.fila + df
            nueva_col = self.col + dc
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.es_pared():
                    # Si es movimiento diagonal, revisamos bloqueos
                    if abs(df) == 1 and abs(dc) == 1:
                        nodo1 = grid[self.fila][self.col + dc]
                        nodo2 = grid[self.fila + df][self.col]
                        if nodo1.es_pared() or nodo2.es_pared():
                            continue  # Bloqueamos movimiento diagonal si hay paredes adyacentes
                    self.vecinos.append((vecino, costo))


def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho, fuente):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana, fuente)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(nodo1, nodo2):
    dx = abs(nodo1.fila - nodo2.fila)
    dy = abs(nodo1.col - nodo2.col)
    return 10 * (dx + dy)

def a_estrella(dibujar, grid, inicio, fin):
    for fila in grid:
        for nodo in fila:
            nodo.actualizar_vecinos(grid)

    contador = 0
    open_set = []
    heapq.heappush(open_set, (0, contador, inicio))
    came_from = {}

    inicio.g = 0
    inicio.h = heuristica(inicio, fin)
    inicio.f = inicio.h

    open_set_hash = {inicio}

    while open_set:
        pygame.time.delay(50)  # Controla velocidad animación
        dibujar()
        actual = heapq.heappop(open_set)[2]
        open_set_hash.remove(actual)

        if actual == fin:
            print("Camino encontrado, reconstruyendo...")
            while actual in came_from:
                actual = came_from[actual]
                actual.hacer_camino()
                dibujar()
                pygame.time.delay(30)  # Animación del camino final
            return True

        for vecino, costo in actual.vecinos:
            temp_g = actual.g + costo
            if temp_g < vecino.g:
                came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h

                if vecino not in open_set_hash:
                    contador += 1
                    heapq.heappush(open_set, (vecino.f, contador, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()

    print("No se encontró camino.")
    return False

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho, FUENTE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Barra espaciadora presionada.")
                    if inicio and fin:
                        print("Inicio y fin definidos, ejecutando A*.")
                        resultado = a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho, FUENTE), grid, inicio, fin)
                        if resultado:
                            print("Camino trazado correctamente.")
                        else:
                            print("No se pudo encontrar camino.")
                    else:
                        print("Define inicio y fin antes de ejecutar A*.")

                if event.key == pygame.K_c:
                    print("Reiniciando grid.")
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
