# Actividad-020425: Aspectos para un Sistema de Acceso con Detección de Rostro

Si quiero usar la detección de rostro como método de acceso, tengo que pensar **qué tan seguro es** y qué necesito para que no se pueda engañar tan fácil. No basta con que reconozca una cara, también debe saber si esa cara es **real y está viva**, y que no sea una foto, video o máscara.

Entonces hice una lista de cosas que debo considerar si quiero que el sistema sea **viable y no vulnerable**:

---

## 1. Protección contra ataques y suplantaciones

- **Detección de vida (liveness detection)**:
  - Revisar si hay movimiento real: parpadeos, sonrisas, cambios en expresión.
  - También se pueden usar sensores especiales (3D, IR, térmicos) si se necesita más seguridad.

- **Evitar que se engañe con fotos o videos**:
  - Pedirle al usuario que haga un gesto aleatorio (abrir la boca, girar la cabeza).
  - Verificar textura y profundidad del rostro.

- **Resistencia física**:
  - Cámaras protegidas contra sabotaje (tapar el lente, cambiar la luz).
  - Que el sistema se bloquee si detecta algo raro.

- **Autenticación multifactor (por si falla algo)**:
  - Además del rostro, usar PIN, tarjeta o huella para mayor seguridad.

---

## 2. Precisión y evitar sesgos

- **Dataset variado**:
  - Entrenar el modelo con muchas caras diferentes: edades, tonos de piel, géneros, etc.

- **Evitar falsos positivos y falsos negativos**:
  - Que no deje pasar a quien no es (ni bloquee a quien sí).
  - Probar el sistema en diferentes condiciones para asegurarse que funcione bien.

- **Actualizar el modelo con el tiempo**:
  - Por si cambia la persona (gafas nuevas, barba, peinado) o el entorno.

---

## 3. Experiencia de usuario (UX)

- **Que funcione rápido**:
  - Idealmente que detecte la cara en menos de 1 segundo.

- **Que tenga respaldo si falla**:
  - Si no detecta la cara, que dé opción de usar QR, tarjeta o contraseña.

- **Accesibilidad**:
  - Que funcione con personas que usan cubrebocas o que no pueden mover el rostro fácilmente.

---

## 4. Infraestructura y seguridad técnica

- **Proteger los dispositivos**:
  - Cámaras seguras, firmware actualizado y sin modificaciones.

- **Redes protegidas**:
  - Usar VPN o VLAN, cifrado de datos, y monitoreo constante para detectar ataques.

- **Registro de accesos**:
  - Guardar quién entró y cuándo, y también los intentos fallidos.

---

## 5. Condiciones del entorno

- **Que funcione en distintos lugares**:
  - Luz baja, sol directo, interiores, exteriores.

- **Consumo eficiente**:
  - Que no gaste demasiada energía si va a estar activo todo el tiempo.

---

## Conclusión

Si quiero que un sistema de acceso con reconocimiento facial funcione bien, **no basta con detectar una cara**. Tiene que saber si es real, proteger los datos, resistir ataques y funcionar para todos los usuarios. También debe tener un buen diseño para que **no incomode a quien lo usa**, y opciones de respaldo si algo falla.

