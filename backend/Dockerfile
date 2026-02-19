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

# Porta fixa 8000 — deve coincidir com EXPOSE e Railway Networking
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
