breast-cancer-ml-api 🎗️
Contenerización de una API de Clasificación de Cáncer de Mama (Docker + CI/CD)
Este proyecto implementa una API RESTful simple utilizando Flask para exponer un modelo de Machine Learning (Random Forest Classifier), entrenado con el dataset de Cáncer de Mama (Wisconsin). El objetivo principal es demostrar un flujo de Contenerización con Docker y CI/CD Automatizado (GitHub Actions).

🚀 Tecnologías Clave
Lenguaje: Python 3.10

Framework: Flask

Modelo ML: Scikit-learn (Random Forest Classifier)

Contenerización: Docker

Automatización: GitHub Actions (CI/CD)

🛠️ Estructura del Proyecto
api-ml-cancer/
├── .github/
│   └── workflows/
│       └── main.yml      # Configuración de CI/CD para Build, Test y Push.
├── api.py                # Código principal de la API de Flask y lógica de carga del modelo.
├── data.csv              # Dataset de Cáncer de Mama (fuente: UCI/sklearn).
├── Dockerfile            # Instrucciones para construir la imagen de Docker.
├── model_cancer.pkl      # Modelo serializado (RandomForestClassifier).
├── requirements.txt      # Dependencias de Python.
└── README.md             # Este archivo.
🐳 Ejecución Local con Docker
Sigue estos pasos para construir la imagen y probar la API en tu máquina local (requiere Docker Desktop).

1. Construir la Imagen
Asegúrate de estar en el directorio raíz del proyecto y ejecuta:
docker build -t cancer-api .

En caso de contenedor previo abierto 
docker ps  # Para ver el ID de tu contenedor en ejecución
docker stop <ID_DEL_CONTENEDOR>  # Para cerrar ejecución 

2. Ejecutar el Contenedor
Ejecuta el contenedor, mapeando el puerto 5000:
(Prueba servicio desde nueva terminal)
docker run -p 5000:5000 -d cancer-api

3. Prueba de Endpoints (Validación)
Puedes usar Invoke-WebRequest (PowerShell) o curl para interactuar con la API.

3.1. Health Check (GET /)
Verifica que el servicio está activo:
Invoke-WebRequest -Method Get -Uri http://localhost:5000/
Respuesta esperada: {"message": "API de Clasificación de Cáncer de Mama", "status": "OK"}

3.2. Predicción (POST /predict)
Envía un ejemplo de 30 features (valores numéricos) para obtener una predicción (0: Benigno, 1: Maligno).
(Probar prediccion desde una nueva terminal)
Invoke-WebRequest -Method Post -Uri http://localhost:5000/predict -ContentType "application/json" -Body '{"features":[17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
Respuesta esperada: {"prediction_code":1,"prediction_text":"Maligno (Alto Riesgo)"}

🔁 CI/CD Automatizado (GitHub Actions)
Este repositorio utiliza GitHub Actions para automatizar el ciclo de vida del contenedor. Cada vez que se realiza un push a la rama main, se ejecuta el siguiente workflow:

Build: Se construye la imagen Docker (cancer-api).

Test: Se ejecuta el contenedor y se prueban los endpoints / (GET) y /predict (POST) con datos de ejemplo para asegurar la funcionalidad del modelo.

Push: Si las pruebas son exitosas, la imagen se etiqueta y se sube automáticamente a Docker Hub (o al registro configurado en los Repository Secrets).