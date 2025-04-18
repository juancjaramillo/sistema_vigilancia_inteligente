# main.py
import cv2, numpy as np, imutils, argparse
import mysql.connector
import easyocr
from centroid_tracker import CentroidTracker

# 1) Parámetros de conexión por línea de comandos
ap = argparse.ArgumentParser()
ap.add_argument("--host",     required=True, help="Host MySQL")
ap.add_argument("--user",     required=True, help="Usuario MySQL")
ap.add_argument("--password", required=True, help="Password MySQL")
ap.add_argument("--database", required=True, help="Base de datos MySQL")
args = ap.parse_args()

# 2) Conexión a MySQL
db = mysql.connector.connect(
    host=args.host,
    user=args.user,
    password=args.password,
    database=args.database
)
cursor = db.cursor()

# 3) Carga modelo MobileNet-SSD
net = cv2.dnn.readNetFromCaffe(
    "models/MobileNetSSD_deploy.prototxt",
    "models/MobileNetSSD_deploy.caffemodel"
)
CLASSES = [
    "background","aeroplane","bicycle","bird","boat",
    "bottle","bus","car","cat","chair","cow","diningtable",
    "dog","horse","motorbike","person","pottedplant",
    "sheep","sofa","train","tvmonitor"
]

# 4) Definición de clases y colores
TARGET_CLASSES = {"person","bicycle","car","bus","train","motorbike"}
PLATE_CLASSES  = {"car","motorbike"}
COLORS = {
    "person":   (  0,255,  0),
    "bicycle":  (255,  0,  0),
    "car":      (  0,  0,255),
    "bus":      (  0,255,255),
    "train":    (255,  0,255),
    "motorbike":(255,255,  0)
}

# 5) Tracker, OCR y cascade de placas
tracker = CentroidTracker()
reader  = easyocr.Reader(['en'], gpu=False)
plate_cascade = cv2.CascadeClassifier(
    "models/haarcascade_russian_plate_number.xml"
)

# 6) Captura de vídeo
vs = cv2.VideoCapture(0)

while True:
    ret, frame = vs.read()
    if not ret:
        break
    frame = imutils.resize(frame, width=600)
    (H, W) = frame.shape[:2]

    # 7) Detección con DNN
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()

    rects, labels = [], []
    for i in range(detections.shape[2]):
        conf = detections[0, 0, i, 2]
        if conf < 0.5:
            continue
        idx = int(detections[0, 0, i, 1])
        label = CLASSES[idx]
        if label not in TARGET_CLASSES:
            continue

        box = (detections[0, 0, i, 3:7] * [W, H, W, H]).astype("int")
        (startX, startY, endX, endY) = box
        rects.append((startX, startY, endX, endY))
        labels.append(label)

        # Dibuja bounding box y etiqueta
        color = COLORS[label]
        text  = f"{label}: {conf:.2f}"
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(frame, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 8) Tracking de centroides
    objects = tracker.update(rects)

    # 9) Procesa cada objeto detectado
    for ((objectID, centroid), label) in zip(objects.items(), labels):
        # Centroid marker
        cv2.circle(frame, tuple(centroid), 4, (255,255,255), -1)
        cv2.putText(frame, f"ID {objectID}",
                    (centroid[0]-10, centroid[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        # Si es coche o moto, intenta leer la placa
        if label in PLATE_CLASSES:
            idx = list(objects.keys()).index(objectID)
            (sx, sy, ex, ey) = rects[idx]
            roi = frame[sy:ey, sx:ex]
            plates = plate_cascade.detectMultiScale(roi, 1.1, 10)
            for (px, py, pw, ph) in plates:
                plate_img = roi[py:py+ph, px:px+pw]
                texts = reader.readtext(plate_img, detail=0)
                if not texts:
                    continue
                placa = texts[0].replace(" ", "")
                # Inserta en MySQL (si no existe ya)
                cursor.execute(
                    "INSERT IGNORE INTO plates (object_id,label,plate) VALUES (%s,%s,%s)",
                    (objectID, label, placa)
                )
                db.commit()
                # Dibuja rectángulo y texto de la placa
                cv2.rectangle(frame,
                              (sx+px, sy+py),
                              (sx+px+pw, sy+py+ph),
                              (0,165,255), 2)
                cv2.putText(frame, placa,
                            (sx+px, sy+py-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0,165,255), 2)

    # 10) Mostrar y salir
    cv2.imshow("Vigilancia Inteligente", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
