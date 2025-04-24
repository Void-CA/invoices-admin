FROM python:3.12

WORKDIR /app

# Instala dependencias del sistema incluyendo CUPS y Ghostscript
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ghostscript \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la app
COPY . .


# Expone el puerto de Django
EXPOSE 8000

# Usa el script de entrada
CMD ["/entrypoint.sh"]
