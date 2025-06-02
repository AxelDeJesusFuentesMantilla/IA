import pygame
import random

# Librerias necearias para el entrenamiento del modelo por vecinos cercanos
import numpy as np 
from sklearn.neighbors import KNeighborsClassifier

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
bala2 = None
fondo = None
nave = None
nave2 = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de movimiento
delantero = False 
delantero_direccion = 9 
delantero_velocidad = 1 
en_posicion_inicial = True 
regresando = False

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('pygamesc/assets/sprites/mono_frame_1.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_2.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_3.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('pygamesc/assets/game/ufo.png')
menu_img = pygame.image.load('pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
bala2 = pygame.Rect(50, 0, 16, 16)  # Rectángulo de la bala
nave = pygame.Rect(w - 100, h - 100, 64, 64)
nave2 = pygame.Rect(20, 0, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para la bala2
velocidad_bala2 = -10  # Velocidad de la bala hacia abajo
bala_disparada2 = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-5, -1)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True
        
# Funcion para disparar la bala2
def disparar_bala2():
    global bala_disparada2, velocidad_bala2
    if not bala_disparada2:
        velocidad_bala2 = 4  # Velocidad aleatoria negativa para la bala
        bala_disparada2 = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False
    
# Función para reiniciar la posición de la bala2
def reset_bala2():
    global bala2, bala_disparada2
    bala2.x = 50  # Reiniciar la posición de la bala2
    bala2.y = 0
    bala_disparada2 = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True
            
def manejar_movimiento_delantero():
    global jugador, delantero, regresando, delantero_direccion, en_posicion_inicial

    if delantero and not regresando:
        # Movimiento hacia adelante
        jugador.x += delantero_direccion

        # Límite hacia adelante
        if jugador.x >= w - 670:
            jugador.x = w - 670
            regresando = True  # Comenzar regreso

    elif regresando:
        # Movimiento de regreso animado
        jugador.x -= delantero_direccion

        # Si llega a la posición inicial, detener
        if jugador.x <= 50:
            jugador.x = 50
            regresando = False
            delantero = False
            en_posicion_inicial = True
            
        
# Función para actualizar el juego
def update():
    global bala, bala2, velocidad_bala, velocidad_bala2,  current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))
    
    # Dibujar la nave superior
    pantalla.blit(nave_img, (nave2.x, nave2.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))
    
    # Mover y dibujar la bala2
    if bala_disparada2:
        bala2.y += velocidad_bala2
        
    # Si la bala2 sale de la pantalla, reiniciar su posición
    if bala2.y > h:
        reset_bala2()
        
    pantalla.blit(bala_img, (bala2.x, bala2.y))
        

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú
        
    # Colisión entre la bala2 y el jugador
    if jugador.colliderect(bala2):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, bala2, velocidad_bala, velocidad_bala2, salto, delantero
    distancia = abs(jugador.x - bala.x)
    distancia2 = abs(jugador.y - bala2.y)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    delantero_hecho = 1 if delantero else 0  # 1 si se movió hacia adelante, 0 si no se movió
    
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho, velocidad_bala2, distancia2, delantero_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                # Cambios agregados, si se presiona la tecla A se inicia el modo automatico
                if evento.key == pygame.K_a:
                    entrenar_modelo() # Se llama a la funcion para entrenar el modelo con los datos recopilados de la partida anterior
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    datos_modelo.clear()  # Limpiar dataset
                    global modelo
                    modelo =  KNeighborsClassifier(n_neighbors=3)
                    print("Modo manual activado. Datos anteriores y modelo reiniciados.")
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, bala2, nave, nave2, bala_disparada, bala_disparada2, salto, en_suelo
    global en_posicion_inicial, delantero, regresando
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    nave2.x, nave2.y = 20, 0  # Reiniciar posición de la nave2
    bala2.x = 50  # Reiniciar posición de la bala2
    bala2.y = 0  # Reiniciar posición de la bala2
    bala_disparada = False
    bala_disparada2 = False  # Reiniciar estado de la bala
    en_posicion_inicial = True  # Reiniciar posición inicial
    delantero = False  # Reiniciar movimiento delantero
    regresando = False  # Reiniciar movimiento de regreso
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    for dato in datos_modelo:
        print("Datos del modelo: ",len(datos_modelo))
        print("Datos recopilados: ", " ", dato)
    #print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    
    

    
    
# Cambios realizados para el programa phaser en python -------------------
modelo_nn = None  # Se inicializa el modelo de vecinos cercanos como None
modelo_nn_delantero = None  # Se inicializa el modelo de vecinos cercanos como None

# Creamos una funcion para entrenar el modelo de vecinos cercanos
def entrenar_modelo():
    global modelo_nn, modelo_nn_delantero

    if len(datos_modelo) < 5:
        print("No hay suficientes datos para entrenar.")
        return

    print("Entrenando modelos de vecinos cercanos con", len(datos_modelo), "datos...")

    # Datos para salto
    X_salto = np.array([[v, d] for v, d, _, _, _, _ in datos_modelo])
    Y_salto = np.array([s for _, _, s, _, _, _ in datos_modelo])

    # Datos para movimiento delantero
    X_delantero = np.array([[v2, d2] for _, _, _, v2, d2, _ in datos_modelo])
    Y_delantero = np.array([m for _, _, _, _, _, m in datos_modelo])

    # Entrenar los clasificadores k-NN (usaremos k=3 por defecto)
    modelo_nn = KNeighborsClassifier(n_neighbors=3)
    modelo_nn.fit(X_salto, Y_salto)

    modelo_nn_delantero = KNeighborsClassifier(n_neighbors=3)
    modelo_nn_delantero.fit(X_delantero, Y_delantero)

    print("Modelos de vecinos cercanos entrenados.")



# Función para decidir si el jugador debe saltar automáticamente basado en el modelo 
def decidir_salto_auto():
    global velocidad_bala, jugador, bala, modelo_nn

    if modelo_nn is None:
        print("Modelo no entrenado.")
        return False

    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad_bala, distancia]])
    prediccion = modelo_nn.predict(entrada)[0]

    return prediccion == 1

def decidir_delantero_auto():
    global velocidad_bala2, jugador, bala2, modelo_nn_delantero

    if modelo_nn_delantero is None:
        print("Modelo de avance no entrenado.")
        return False

    distancia2 = abs(jugador.y - bala2.y)
    entrada = np.array([[velocidad_bala2, distancia2]])
    prediccion = modelo_nn_delantero.predict(entrada)[0]

    return prediccion == 1




# Fin cambios realizados --------------------------


def main():
    global salto, en_suelo, bala_disparada, bala_disparada2, delantero, en_posicion_inicial

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_LCTRL or evento.key == pygame.K_RCTRL:  # Detectar la tecla Ctrl
                    delantero = True  # Cambiar la variable de movimiento a True
                    en_posicion_inicial = False  # Cambiar la variable de posición inicial a False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Cambios realizados, se agregó el modo automático 
            if modo_auto:
                # Decidir si saltar automáticamente a traves de la funcion decidir_salto_auto
                if en_suelo and decidir_salto_auto():
                    salto = True
                    en_suelo = False
                if salto:
                    manejar_salto()
                    
                # Decidir si moverse hacia adelante automáticamente a traves de la funcion decidir_delantero_auto
                if en_posicion_inicial and decidir_delantero_auto():
                    delantero = True
                    en_posicion_inicial = False
                if delantero:
                    manejar_movimiento_delantero()
                    
            else: # Modo manual: el jugador controla el salto
                if salto:
                    manejar_salto()
                
                if delantero:
                    manejar_movimiento_delantero()
                
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()
            
            if not bala_disparada2:
                disparar_bala2()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
