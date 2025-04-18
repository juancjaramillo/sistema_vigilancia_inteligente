# Sistema de Vigilancia Inteligente

**Detección y seguimiento en tiempo real de personas y vehículos**, con captura automática de matrículas y almacenamiento en MySQL.

---

## 🔍 Descripción

Este proyecto implementa un sistema de visión artificial para:

1. **Detección** de objetos en 6 clases: personas, bicicletas, coches, autobuses, trenes y motocicletas.
2. **Seguimiento** de centroides para mantener un ID único de cada objeto entre fotogramas.
3. **Reconocimiento de matrículas** (coches y motos) mediante cascada Haar y EasyOCR.
4. **Almacenamiento** de matrículas detectadas en una base de datos MySQL.

Es ideal para aplicaciones de vigilancia, control de tráfico y gestión de accesos.

---

## 📁 Estructura del proyecto

```bash
sistema_vigilancia_inteligente/
├── .gitignore
├── README.md
├── requirements.txt
├── db_init.sql                # Script MySQL para crear BD y tabla
├── centroid_tracker.py        # Lógica de tracking por centroides
├── main.py                    # Núcleo de detección, OCR y guardado
└── models/
    ├── MobileNetSSD_deploy.prototxt
    ├── MobileNetSSD_deploy.caffemodel
    └── haarcascade_russian_plate_number.xml
```

---

## 📋 Prerrequisitos

- Python 3.7 o superior
- MySQL Server
- Webcam o cámara USB

---

## ⚙️ Instalación y configuración

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/sistema_vigilancia_inteligente.git
   cd sistema_vigilancia_inteligente
   ```

2. **Crea y activa un entorno virtual**:
   ```powershell
   # Windows (PowerShell)
   py -3 -m venv venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\Activate.ps1
   ```
   ```bash
   # Unix/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. **Crea la base de datos y la tabla**:
   - Edita `db_init.sql` si necesitas ajustar el nombre de la BD.
   - Ejecuta:
     ```bash
     mysql -u <TU_USUARIO> -p < db_init.sql
     ```
   Esto creará la base `vigilancia` y la tabla `plates`.

5. **Descarga los modelos** en `models/` si no están incluidos:
   - MobileNetSSD_deploy.prototxt
   - MobileNetSSD_deploy.caffemodel
   - haarcascade_russian_plate_number.xml

---

## ▶️ Uso

Con el entorno virtual activo, ejecuta:

```bash
python main.py \
  --host localhost \
  --user tu_usuario \
  --password tu_password \
  --database vigilancia
```

- Se abrirá una ventana con el feed de la cámara.
- Detectará y dibujará recuadros de color distinto para cada clase.
- Mantendrá un **ID** (“ID #”) sobre cada objeto.
- Si detecta un coche o moto, extraerá la matrícula y la almacenará en MySQL.
- Presiona **q** para cerrar la aplicación.

---

## 🖥️ Código de ejemplo

```python
# Fragmento de main.py (detección y guardado de matrículas)
import cv2, imutils
import mysql.connector
import easyocr
from centroid_tracker import CentroidTracker

# Conexión MySQL
db = mysql.connector.connect(host="localhost", user="root", password="root", database="vigilancia")
cursor = db.cursor()

# Carga modelo DNN
net = cv2.dnn.readNetFromCaffe("models/MobileNetSSD_deploy.prototxt", "models/MobileNetSSD_deploy.caffemodel")
# Clases e inicializaciones...

# Bucle principal
enabled, vs = True, cv2.VideoCapture(0)
while enabled:
    ret, frame = vs.read()
    # detección, tracking y OCR...
    # inserción en la tabla plates
```

---

## 💾 Base de datos MySQL (`db_init.sql`)

```sql
CREATE DATABASE IF NOT EXISTS vigilancia
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE vigilancia;

CREATE TABLE IF NOT EXISTS plates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  object_id INT NOT NULL,
  label VARCHAR(20) NOT NULL,
  plate VARCHAR(20) NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_plate (object_id, plate)
) ENGINE=InnoDB;
```

---

## 🔧 Configuración adicional

- Ajusta **`maxDisappeared`** y **`maxDistance`** en `centroid_tracker.py` para adaptarlo a tu cámara.
- Modifica la confianza mínima (`0.5`) para detecciones más o menos estrictas.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un _issue_ o _pull request_.

---

## 📝 Licencia

MIT License. Consulta `LICENSE` para más detalles.

