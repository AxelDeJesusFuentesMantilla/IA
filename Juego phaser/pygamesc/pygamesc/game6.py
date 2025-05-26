import pygame
import random
import numpy as np
import os
import joblib
from datetime import datetime
from tensorflow.keras.models import save_model, load_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Inicializar Pygame
pygame.init()

# Dimensiones y configuración inicial
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego IA: Disparo, Salto, Nave y Modelos ML")

# Paleta de colores
COLORES = {
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "VERDE": (0, 255, 0),
    "ROJO": (255, 0, 0),
    "AZUL": (0, 0, 255)
}

# Variables de estado del juego
estado_juego = {
    "salto": False,
    "salto_altura": 15,
    "gravedad": 1,
    "en_suelo": True,
    "jump_initiated": False,
    "pausa": False,
    "menu_activo": True,
    "modo_auto": False,
    "modelo_seleccionado": None,
    "bala_disparada": False,
    "velocidad_bala": -10,
    "datos_modelo": [],
    "modelo_dt": None,
    "modelo_nn": None,
    "dt_entrenado": False,
    "nn_entrenado": False
}

# Configuración de modelos
CONFIG_MODELOS = {
    "ruta_dt": 'decision_tree_model.pkl',
    "ruta_nn": 'neural_network_model.h5',
    "ultimo_entrenamiento_dt": None,
    "ultimo_entrenamiento_nn": None
}

# Elementos del juego
elementos = {
    "jugador": pygame.Rect(50, h - 100, 32, 48),
    "bala": pygame.Rect(w - 50, h - 90, 16, 16),
    "nave": pygame.Rect(w - 100, h - 100, 64, 64),
    "fondo_x1": 0,
    "fondo_x2": w,
    "frame_actual": 0,
    "contador_frames": 0,
    "velocidad_animacion": 10
}

# Carga de recursos
try:
    recursos = {
        "jugador": [
            pygame.image.load(f'assets/sprites/mono_frame_{i}.png') for i in range(1,5)
        ],
        "bala": pygame.image.load('assets/sprites/purple_ball.png'),
        "fondo": pygame.transform.scale(pygame.image.load('assets/game/fondo2.png'), (w, h)),
        "nave": pygame.image.load('assets/game/ufo.png')
    }
except Exception as e:
    print(f"Error cargando recursos: {e}")
    pygame.quit()
    exit()

# Funciones del juego
def manejar_disparo():
    if not estado_juego["bala_disparada"]:
        estado_juego["velocidad_bala"] = random.randint(-15, -5)
        elementos["bala"].y = h - 90 - random.randint(0, 20)
        estado_juego["bala_disparada"] = True

def reiniciar_bala():
    elementos["bala"].x = w - 50
    estado_juego["bala_disparada"] = False

def actualizar_salto():
    if estado_juego["salto"]:
        elementos["jugador"].y -= estado_juego["salto_altura"]
        estado_juego["salto_altura"] -= estado_juego["gravedad"]
        if elementos["jugador"].y >= h - 100:
            elementos["jugador"].y = h - 100
            estado_juego["salto"] = False
            estado_juego["salto_altura"] = 15
            estado_juego["en_suelo"] = True

# Funciones de IA
def entrenar_arbol_decision():
    if len(estado_juego["datos_modelo"]) < 50:
        print("Datos insuficientes para entrenar el modelo")
        return False

    X = np.array([[d[0], d[1]] for d in estado_juego["datos_modelo"]])
    y = np.array([d[2] for d in estado_juego["datos_modelo"]])

    if len(np.unique(y)) < 2:
        print("Datos no balanceados")
        return False

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    modelo = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5)
    modelo.fit(X_train, y_train)
    
    # Guardar y actualizar estado
    joblib.dump(modelo, CONFIG_MODELOS["ruta_dt"])
    estado_juego["modelo_dt"] = modelo
    estado_juego["dt_entrenado"] = True
    CONFIG_MODELOS["ultimo_entrenamiento_dt"] = datetime.now()
    return True

def entrenar_red_neuronal():
    if len(estado_juego["datos_modelo"]) < 50:
        print("Datos insuficientes para entrenar el modelo")
        return False

    X = np.array([[d[0], d[1]] for d in estado_juego["datos_modelo"]])
    y = np.array([d[2] for d in estado_juego["datos_modelo"]])

    modelo = Sequential([
        Dense(8, input_dim=2, activation='relu'),
        Dense(4, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X, y, epochs=50, verbose=0)
    
    # Guardar y actualizar estado
    save_model(modelo, CONFIG_MODELOS["ruta_nn"])
    estado_juego["modelo_nn"] = modelo
    estado_juego["nn_entrenado"] = True
    CONFIG_MODELOS["ultimo_entrenamiento_nn"] = datetime.now()
    return True

def cargar_modelos():
    try:
        estado_juego["modelo_dt"] = joblib.load(CONFIG_MODELOS["ruta_dt"])
        estado_juego["dt_entrenado"] = True
        print("Modelo DT cargado")
    except:
        estado_juego["dt_entrenado"] = False

    try:
        estado_juego["modelo_nn"] = load_model(CONFIG_MODELOS["ruta_nn"])
        estado_juego["nn_entrenado"] = True
        print("Modelo NN cargado")
    except:
        estado_juego["nn_entrenado"] = False

# Sistema de menús
def mostrar_menu_principal():
    fuente = pygame.font.SysFont('Arial', 24)
    fuente_titulo = pygame.font.SysFont('Arial', 30, bold=True)
    
    while estado_juego["menu_activo"]:
        pantalla.fill(COLORES["NEGRO"])
        
        # Opciones del menú
        opciones = [
            ("MODO DE JUEGO", True),
            ("1 - Modo Manual", False),
            ("2 - Modo Automático DT", False),
            ("3 - Modo Automático NN", False),
            ("", True),
            ("ENTRENAMIENTO", True),
            ("T - Entrenar DT", False),
            ("Y - Entrenar NN", False),
            ("C - Limpiar Datos", False),
            ("", True),
            ("Q - Salir", False)
        ]
        
        # Renderizado
        y = 50
        for texto, es_titulo in opciones:
            if es_titulo:
                render = fuente_titulo.render(texto, True, COLORES["VERDE"])
            else:
                render = fuente.render(texto, True, COLORES["BLANCO"])
            pantalla.blit(render, (w//2 - render.get_width()//2, y))
            y += 40 if es_titulo else 30
        
        pygame.display.flip()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                manejar_input_menu(evento.key)

def manejar_input_menu(tecla):
    if tecla == pygame.K_1:
        estado_juego["modo_auto"] = False
        estado_juego["menu_activo"] = False
    elif tecla == pygame.K_2:
        if estado_juego["dt_entrenado"]:
            estado_juego["modo_auto"] = True
            estado_juego["modelo_seleccionado"] = 'dt'
            estado_juego["menu_activo"] = False
    elif tecla == pygame.K_3:
        if estado_juego["nn_entrenado"]:
            estado_juego["modo_auto"] = True
            estado_juego["modelo_seleccionado"] = 'nn'
            estado_juego["menu_activo"] = False
    elif tecla == pygame.K_t:
        entrenar_arbol_decision()
    elif tecla == pygame.K_y:
        entrenar_red_neuronal()
    elif tecla == pygame.K_c:
        estado_juego["datos_modelo"] = []
    elif tecla == pygame.K_q:
        pygame.quit()

# Bucle principal del juego
def ejecutar_juego():
    reloj = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and estado_juego["en_suelo"]:
                    estado_juego["salto"] = True
                    estado_juego["en_suelo"] = False
                    estado_juego["jump_initiated"] = True
        
        # Lógica de actualización
        if not estado_juego["menu_activo"] and not estado_juego["pausa"]:
            actualizar_estado_juego()
        
        # Renderizado
        dibujar_elementos()
        reloj.tick(30)

def actualizar_estado_juego():
    # Movimiento del fondo
    elementos["fondo_x1"] -= 2
    elementos["fondo_x2"] -= 2
    if elementos["fondo_x1"] <= -w:
        elementos["fondo_x1"] = w
    if elementos["fondo_x2"] <= -w:
        elementos["fondo_x2"] = w

    # Movimiento de la bala
    if estado_juego["bala_disparada"]:
        elementos["bala"].x += estado_juego["velocidad_bala"]
        if elementos["bala"].x < 0:
            reiniciar_bala()
            if not estado_juego["modo_auto"]:
                manejar_disparo()

    # Lógica de salto
    actualizar_salto()

    # Detección de colisiones
    if elementos["jugador"].colliderect(elementos["bala"]):
        reiniciar_juego()

def dibujar_elementos():
    pantalla.blit(recursos["fondo"], (elementos["fondo_x1"], 0))
    pantalla.blit(recursos["fondo"], (elementos["fondo_x2"], 0))
    
    # Dibujar personaje
    pantalla.blit(recursos["jugador"][elementos["frame_actual"]], 
                (elementos["jugador"].x, elementos["jugador"].y))
    
    # Actualizar animación
    elementos["contador_frames"] += 1
    if elementos["contador_frames"] >= elementos["velocidad_animacion"]:
        elementos["frame_actual"] = (elementos["frame_actual"] + 1) % 4
        elementos["contador_frames"] = 0

    # Dibujar otros elementos
    pantalla.blit(recursos["nave"], (elementos["nave"].x, elementos["nave"].y))
    if estado_juego["bala_disparada"]:
        pantalla.blit(recursos["bala"], (elementos["bala"].x, elementos["bala"].y))
    
    pygame.display.flip()

def reiniciar_juego():
    elementos["jugador"].x, elementos["jugador"].y = 50, h - 100
    elementos["bala"].x = w - 50
    estado_juego.update({
        "salto": False,
        "en_suelo": True,
        "bala_disparada": False
    })

# Inicialización y ejecución
if __name__ == "__main__":
    cargar_modelos()
    mostrar_menu_principal()
    ejecutar_juego()
    pygame.quit()