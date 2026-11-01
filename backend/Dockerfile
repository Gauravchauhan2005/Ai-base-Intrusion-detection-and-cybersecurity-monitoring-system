FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for C-extensions, PostgreSQL, and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, ml pipeline and producer for attack simulation
COPY backend/ /app/
COPY ml/ /app/ml/
COPY producer/ /app/producer/

ENV PYTHONPATH=/app:.

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
