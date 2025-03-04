# Stage 1: Build dependencies
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/requirements.txt requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /install /usr/local/
COPY src/ ./src

EXPOSE ${BACKEND_PORT}
CMD ["python", "-m", "src.main"]