FROM python:3.13-slim

WORKDIR /app

EXPOSE 8000

CMD pip install --no-cache-dir -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py dev_db && \
    python manage.py runserver 0.0.0.0:8000
