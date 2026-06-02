# stage 1: build the application

FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# stage 2: create the final image

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY services/ingestion ./services/ingestion
COPY shared/ ./shared
ENV PATH=/root/.local/bin:$PATH
CMD ["python","-m","services.ingestion.main"]