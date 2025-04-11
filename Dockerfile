# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y luego instalar las dependencias
COPY requirements.txt .

RUN apt update && apt install -y \
    ghostscript \
    cups \
    cups-client \
    && apt clean

COPY . /app
WORKDIR /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto al contenedor
COPY . .

# Exponer el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Establecer el comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
