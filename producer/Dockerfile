FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY producer/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared streaming code and producer
COPY backend/app/ /app/app/
COPY producer/ /app/

ENV PYTHONPATH=/app:.

CMD ["python", "replay_traffic.py"]
