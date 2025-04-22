FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ghostscript \
    cups \
    cups-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Reemplaza 'tu_proyecto' por el nombre real del proyecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
