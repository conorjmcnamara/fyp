FROM python:3.10-slim

WORKDIR /app

COPY requirements/base.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ ./src

CMD ["python", "-m", "src.main"]