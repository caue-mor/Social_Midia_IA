FROM python:3.12-slim

WORKDIR /app

# Instala dependencias do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codigo
COPY . .

# Expoe porta
EXPOSE 8000

# Usa $PORT do Railway (definir PORT=8000 nas env vars do Railway)
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
