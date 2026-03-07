FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

ENV PYTHONPATH=/app/services/doctor_service

COPY . /app

# The command will be run from docker-compose, but we provide a default here
CMD ["sys.path.append('.')", "uvicorn", "services.doctor_service.app.main:app", "--host", "0.0.0.0", "--port", "8003"]
