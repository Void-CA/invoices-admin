FROM python:3.12-slim

WORKDIR /app

# Instala solo lo esencial (si necesitas compilar alguna dependencia nativa)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 \
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
