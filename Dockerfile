FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app
USER app

VOLUME ["/app/data", "/app/content", "/app/reports", "/app/certificates"]

CMD ["python", "-m", "src.hipaa_training.cli"]
