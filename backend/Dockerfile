FROM python:3.12-slim

WORKDIR /app

# Instala dependencias do sistema (build-essential + libs para weasyprint/psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codigo
COPY . .

# Expoe porta
EXPOSE 8000

# Comando de inicializacao (shell form para Railway resolver $PORT)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
