FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema para WeasyPrint y otras herramientas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libcairo2 libcairo2-dev \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libgobject-2.0-0 \
    shared-mime-info \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la app
COPY . .

# Expone el puerto de Django
EXPOSE 8000

# Comando de entrada
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
