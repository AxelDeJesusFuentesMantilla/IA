# Evaluación: Red Neuronal para Detección de Emociones con Landmarks de MediaPipe

## 1. Tipo de red neuronal y descripción de sus partes

Se utilizará una **Red Neuronal Artificial (RNA) de tipo Feedforward (Perceptrón Multicapa, MLP)** para clasificar emociones a partir de landmarks faciales.

### Estructura de la red:

- **Capa de entrada:**  
  Recibe coordenadas (x, y) o (x, y, z) de los landmarks faciales proporcionados por MediaPipe.  
  - Si se usan 468 landmarks 2D: 468 × 2 = **936 entradas**
  - Si se usan 3D: 468 × 3 = **1404 entradas**

- **Capas ocultas:**  
  De 1 a 3 capas densas (*fully connected*), activadas con la función **ReLU**, capaces de capturar relaciones no lineales entre los landmarks.

- **Capa de salida:**  
  Una neurona por clase de emoción. Por ejemplo, para 6 emociones:
  - Alegría
  - Tristeza
  - Enojo
  - Miedo
  - Sorpresa
  - Neutro

---

## 2. Patrones a utilizar

Los patrones de entrada serán las **coordenadas de los landmarks faciales** que proporciona MediaPipe. Adicionalmente, se pueden calcular:

- Distancias entre puntos clave (ej. entre ojos y boca)
- Ángulos entre segmentos (ej. cejas, labios)
- Coordenadas normalizadas para mejorar la generalización del modelo

---

## 3. Función de activación

- **Capas ocultas:**  
  Se utiliza **ReLU (Rectified Linear Unit)** por su eficiencia computacional y buen desempeño en tareas de clasificación.

- **Capa de salida:**
  - **Softmax**, si es clasificación multiclase excluyente (una emoción a la vez)
  - **Sigmoide**, si se permite más de una emoción simultáneamente (clasificación multietiqueta)

---

## 4. Número máximo de entradas

El número máximo de entradas es:

- **936 entradas**, si se utilizan 468 puntos en 2D (x, y)
- **1404 entradas**, si se utilizan 468 puntos en 3D (x, y, z)

---

## 5. Valores esperados a la salida de la red

- Si se utiliza **Softmax**, se espera un **vector de probabilidades** que suma 1. Ejemplo:
  ```python
  [0.05, 0.70, 0.10, 0.05, 0.05, 0.05]
