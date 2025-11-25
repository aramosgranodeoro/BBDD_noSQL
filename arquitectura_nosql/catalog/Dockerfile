# Dockerfile
FROM python:3.10

# Crear y activar el entorno virtual
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar python-multipart
RUN pip install python-multipart

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8001

# Comando para iniciar la aplicación
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
