FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ghostscript \
    cups \
    cups-client \
    libcups2-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Usa runserver en vez de gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
