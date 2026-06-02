# Stage 1: Build the application

FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Create the final image

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY shared/ ./shared
COPY services/query_api ./services/query_api
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn","services.query_api.main:app","--host","0.0.0.0","--port","8000"]