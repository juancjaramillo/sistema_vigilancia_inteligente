# Sistema de Vigilancia Inteligente
Este proyecto implementa un sistema de visión artificial para entornos de seguridad y control de tráfico con las siguientes funcionalidades:

Descripción del proyecto
Sistema de Vigilancia Inteligente
Este proyecto implementa un sistema de visión artificial para entornos de seguridad y control de tráfico con las siguientes funcionalidades:

Detección en tiempo real

Detección y diferenciación de personas, bicicletas, automóviles y autobuses usando MobileNet‑SSD y OpenCV DNN.

Seguimiento de objetos

Tracking de centroides para asignar un ID único a cada objeto y mantener su identificación mientras se mueven en el encuadre.

Reconocimiento de matrículas

Detección de placas vehiculares mediante cascada Haar y lectura de texto con EasyOCR.

Almacenamiento automático de matrículas detectadas en una base de datos SQLite junto con el ID de objeto y marca de tiempo.

Interfaz de control

Funciones de ejemplo para enviar las coordenadas normalizadas y el tipo de objeto a sistemas externos (cámaras PTZ, servomotores, APIs, etc.).

Registro y auditoría

Persiste en disco todas las detecciones de matrículas y permite consultas posteriores sobre quién y cuándo pasó cada vehículo.

Objetivos
Proveer una solución modular y extensible para vigilancia en espacios públicos o privados.

Facilitar la integración con sistemas de control de acceso y administración de flotas.

Generar un registro automático y fiable de eventos de tráfico (acceso de vehículos autorizados, conteo de personas, etc.).
