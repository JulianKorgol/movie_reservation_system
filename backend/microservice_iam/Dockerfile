FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libpq5 \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Non-root user — same UID as prod
RUN addgroup --gid 1001 appgroup && \
    adduser  --uid 1001 --gid 1001 --no-create-home --disabled-password appuser

# Install deps as root into the system site-packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appgroup /app

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Overridden by docker-compose.dev.yml
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
