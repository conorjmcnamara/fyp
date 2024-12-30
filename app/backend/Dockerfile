FROM python:3.10-slim

WORKDIR /app

COPY requirements/base.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ ./src

EXPOSE ${BACKEND_PORT}
CMD uvicorn src.main:app --host 0.0.0.0 --port ${BACKEND_PORT}