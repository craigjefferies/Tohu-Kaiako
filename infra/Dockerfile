FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY backend /app/backend
COPY frontend /app/frontend
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
