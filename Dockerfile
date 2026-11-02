FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

# Development-only server. Do not use this container as a public production checkout.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
