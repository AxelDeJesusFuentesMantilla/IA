import cv2
import mediapipe as mp
import numpy as np
import os
import csv

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2,
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Puntos: ojos, boca, nariz (correctos)
selected_points = [33, 133, 362, 263, 61, 291, 49, 279, 168, 19]  # nariz altura: 168 a 19

folder = "Medidas"
os.makedirs(folder, exist_ok=True)
csv_path = os.path.join(folder, "medidas_facial.csv")

if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "persona",
            "ancho_ojo_izq", "ancho_ojo_der", "ancho_boca",
            "ojos_a_boca", "ojoIzq_a_bocaIzq", "ojoDer_a_bocaDer",
            "prop_ojo_boca", "prop_vertical", "prop_simetria",
            "ancho_nariz", "alto_nariz", "prop_nariz"
        ])

def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    key = cv2.waitKey(1) & 0xFF

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            if all(idx in puntos for idx in selected_points):
                # Distancias base
                ancho_ojo_izq = distancia(puntos[33], puntos[133])
                ancho_ojo_der = distancia(puntos[362], puntos[263])
                ancho_boca = distancia(puntos[61], puntos[291])
                centro_ojos = (
                    int((puntos[33][0] + puntos[362][0]) / 2),
                    int((puntos[33][1] + puntos[362][1]) / 2)
                )
                centro_boca = (
                    int((puntos[61][0] + puntos[291][0]) / 2),
                    int((puntos[61][1] + puntos[291][1]) / 2)
                )
                ojos_a_boca = distancia(centro_ojos, centro_boca)
                ojoIzq_a_bocaIzq = distancia(puntos[33], puntos[61])
                ojoDer_a_bocaDer = distancia(puntos[263], puntos[291])

                promedio_ojos = (ancho_ojo_izq + ancho_ojo_der) / 2
                prop_ojo_boca = ancho_boca / promedio_ojos if promedio_ojos > 0 else 0
                prop_vertical = ojos_a_boca / ancho_boca if ancho_boca > 0 else 0
                prop_simetria = ojoIzq_a_bocaIzq / ojoDer_a_bocaDer if ojoDer_a_bocaDer > 0 else 0

                # Nariz
                ancho_nariz = distancia(puntos[49], puntos[279])
                alto_nariz = distancia(puntos[168], puntos[19])
                prop_nariz = alto_nariz / ancho_nariz if ancho_nariz > 0 else 0

                # Punto de intersección entre ancho y alto de nariz
                punto_medio_nariz = (
                    int((puntos[49][0] + puntos[279][0]) / 2),
                    int((puntos[49][1] + puntos[279][1]) / 2)
                )

                # Mostrar medidas en pantalla
                y0 = 30
                dy = 20
                info = [
                    f"Ojo Izq: {ancho_ojo_izq:.1f}",
                    f"Ojo Der: {ancho_ojo_der:.1f}",
                    f"Boca: {ancho_boca:.1f}",
                    f"Ojos-Boca: {ojos_a_boca:.1f}",
                    f"OIzq-BIzq: {ojoIzq_a_bocaIzq:.1f}",
                    f"ODer-BDer: {ojoDer_a_bocaDer:.1f}",
                    f"P. Ojo-Boca: {prop_ojo_boca:.2f}",
                    f"P. Vertical: {prop_vertical:.2f}",
                    f"P. Simetría: {prop_simetria:.2f}",
                    f"Nariz Ancho: {ancho_nariz:.1f}",
                    f"Nariz Alto: {alto_nariz:.1f}",
                    f"P. Nariz: {prop_nariz:.2f}"
                ]
                for i, text in enumerate(info):
                    cv2.putText(frame, text, (10, y0 + i * dy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 255, 0), 1)

                # Dibujar líneas de nariz
                cv2.line(frame, puntos[49], puntos[279], (0, 255, 255), 1)   # ancho nariz
                cv2.line(frame, puntos[168], puntos[19], (0, 255, 255), 1)   # alto nariz
                cv2.circle(frame, punto_medio_nariz, 3, (0, 0, 255), -1)     # intersección

                # Guardado
                if key == ord('s'):
                    nombre = input("Nombre o ID de la persona: ")
                    try:
                        with open(csv_path, mode="a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                nombre,
                                round(ancho_ojo_izq, 2), round(ancho_ojo_der, 2), round(ancho_boca, 2),
                                round(ojos_a_boca, 2), round(ojoIzq_a_bocaIzq, 2), round(ojoDer_a_bocaDer, 2),
                                round(prop_ojo_boca, 3), round(prop_vertical, 3), round(prop_simetria, 3),
                                round(ancho_nariz, 2), round(alto_nariz, 2), round(prop_nariz, 3)
                            ])
                        print(f"✔ Datos guardados para: {nombre}")
                    except PermissionError:
                        print("❌ No se pudo guardar el archivo. Asegúrate de que no esté abierto.")

    cv2.imshow('Presiona "S" para guardar | "Q" para salir', frame)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
