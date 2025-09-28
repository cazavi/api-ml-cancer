#Instalaciones e importaciones
import joblib
import warnings
import numpy as np
import pandas as pd
import logging
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#No mostrar warnings de modulos
warnings.filterwarnings('ignore')

#-----------Contenerización de una API ML con Docker-----------



# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# No mostrar warnings de módulos
warnings.filterwarnings('ignore')

# ----------- CÓDIGO DE ENTRENAMIENTO (Necesario para generar el modelo) -----------
# NOTA: Este bloque solo necesita ejecutarse una vez para crear 'model_cancer.pkl'.
MODEL_FILENAME = 'model_cancer.pkl'
#1.Entrenamiento del modelo
# Set the path to the file you'd like to load
file_path = "data.csv"

try:
    # Intenta cargar el modelo si ya existe
    model = joblib.load(MODEL_FILENAME)
    logging.info(f"Modelo {MODEL_FILENAME} cargado exitosamente.")
    
    # Dummies para contar features (Asumimos el dataset base para contar las features)
    data_check = pd.read_csv(file_path)
    if 'id' in data_check.columns:
        data_check = data_check.drop('id', axis=1)
    if data_check.columns[-1].startswith('Unnamed'):
        data_check = data_check.iloc[:, :-1]
    
    # Número de features de entrada (total de columnas - 1 columna 'diagnosis')
    N_FEATURES = data_check.shape[1] - 1
    
except FileNotFoundError:
    # Si el modelo no existe, lo entrenamos y guardamos
    logging.warning(f"Modelo {MODEL_FILENAME} no encontrado. Entrenando y guardando...")
    
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error("ERROR CRÍTICO: 'data.csv' no encontrado. Asegurate de descargarlo y colocarlo en la misma carpeta.")
        raise

    # 1. Preprocesamiento (Cáncer de Mama)
    if 'id' in data.columns:
        data = data.drop('id', axis=1)
        
    # Eliminar columna innecesaria si existe (común en datasets de Kaggle)
    if data.columns[-1].startswith('Unnamed'):
        data = data.iloc[:, :-1]
    
    # Conversión de la variable objetivo 'diagnosis' (M=1, B=0)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    
    X = data.drop('diagnosis', axis=1)
    y = data['diagnosis']
    
    # Definir el número de características (30 para este dataset)
    N_FEATURES = X.shape[1] 
    
    # 2. Entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # 3. Guardar modelo
    joblib.dump(model, MODEL_FILENAME)
    logging.info(f"Modelo entrenado y guardado como {MODEL_FILENAME}.")

# ----------------------------------------------------------------------------

# API en Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # GET /: para probar el estado del servicio
    logging.info("Ruta '/' accedida. Estado del servicio OK.")
    return jsonify({
        "status": "OK", 
        "message": "API de Prediccion de Cancer de Mama activa.",
        "model_features": N_FEATURES # Útil para que el usuario sepa cuántas características enviar
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    # POST /predict: para recibir un JSON y retornar predicción
    try:
        data = request.get_json(force=True)
    except Exception:
        logging.error("Fallo al procesar el JSON de entrada.")
        return jsonify({
            "error": "Solicitud JSON no valida. Asegúrese de enviar un JSON bien formado."
        }), 400
    
    # 1. Validación de entradas
    if 'features' not in data:
        logging.error("Entrada JSON no tiene la clave 'features'.")
        return jsonify({
            "error": "JSON debe contener la clave 'features'."
        }), 400

    features = data['features']
    
    # 2. Validación de la dimensión
    if not isinstance(features, list) or len(features) != N_FEATURES:
        logging.error(f"Se esperaban {N_FEATURES} caracteristicas, se recibieron {len(features) if isinstance(features, list) else 'ninguna'}.")
        return jsonify({
            "error": f"Se requieren exactamente {N_FEATURES} valores numericos en la lista 'features' (Breast Cancer Dataset)."
        }), 400

    # 3. Predicción
    try:
        # Convertir a numpy array y darle la forma correcta (1 fila, N_FEATURES columnas)
        features_array = np.array(features, dtype=float).reshape(1, -1)
        prediction_code = model.predict(features_array)[0]
        
        # Mapeo de la predicción
        prediction_text = "Maligno (Alto Riesgo)" if prediction_code == 1 else "Benigno (Bajo Riesgo)"
        
        logging.info("Predicción exitosa.")
        return jsonify({
            "prediction_code": int(prediction_code),
            "prediction_text": prediction_text
        }), 200

    except Exception as e:
        # 4. Manejo de errores (General del modelo o cálculo)
        logging.error(f"Error interno durante la prediccion: {str(e)}")
        # Devuelve un código 500 para errores internos del servidor/modelo
        return jsonify({
            "error": "Error interno del servidor. Revise el log."
        }), 500

if __name__ == '__main__':
    # Flask ya maneja el logging de inicio
    app.run(host='0.0.0.0', port=5000)