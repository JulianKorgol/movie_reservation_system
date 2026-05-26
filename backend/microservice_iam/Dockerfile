# syntax=docker/dockerfile:1

# ═════════════════════════════════════════════════════════════════════════════
# BASE — shared system packages, user, and Python dependencies
# ═════════════════════════════════════════════════════════════════════════════
FROM python:3.13-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libpq5 \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Non-root user — same UID/GID as every other service in the compose stack
RUN addgroup --gid 1001 appgroup && \
    adduser  --uid 1001 --gid 1001 --no-create-home --disabled-password appuser

# Install Python deps as root into system site-packages, then hand over /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    chown -R appuser:appgroup /app

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# ═════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT — Django dev server with auto-reload
# ═════════════════════════════════════════════════════════════════════════════
FROM base AS development

COPY --chown=appuser:appgroup . .

# Overridden by docker-compose.dev.yml command: + bind-mounted source
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000

# ═════════════════════════════════════════════════════════════════════════════
# PRODUCTION — Gunicorn WSGI server (multi-worker, no auto-reload)
# ═════════════════════════════════════════════════════════════════════════════
FROM base AS production

COPY --chown=appuser:appgroup . .

CMD ["gunicorn", "microservice_iam.wsgi:application", \
     "--bind",         "0.0.0.0:8000", \
     "--workers",      "2", \
     "--timeout",      "60", \
     "--access-logfile", "-", \
     "--error-logfile",  "-"]
