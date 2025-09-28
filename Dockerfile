#3. Contenerización
#Escribe un Dockerfile que instale todas las dependencias y ejecute tu app.
#Imagen base
FROM python:3.10-slim
#Directorio de trabajo
WORKDIR /app
#Copiar archivos
COPY requirements.txt .
COPY data.csv .
COPY api.py . 
COPY model_cancer.pkl . 
#Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
#Exponer Puerto
EXPOSE 5000
#Ejecutar app
CMD ["python", "api.py"]
#-------------------
  