import cv2 #opencv
import mediapipe as mp

#iniciar opencv e mediapipe
webcam = cv2.VideoCapture(0)
solucao_reconhecimento_rosto = mp.solutions.face_detection
reconhecedor_rostos = solucao_reconhecimento_rosto.FaceDetection()
desenho = mp.solutions.drawing_utils

while True:
    # ler as informações da webcam
    verificador, frame = webcam.read()
    if not verificador:
        break

    # Reconhecer os rostos que tem ali dentro
    lista_rostos = reconhecedor_rostos.process(frame)

    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            # desenhar os rostos na imagem
            desenho.draw_detection(frame, rosto)

    cv2.imshow("Rosto na webcam", frame)

    # quando apertar ESC, para o loop
    if cv2.waitKey(5) == 27:
        break
            
webcam.release()