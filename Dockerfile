FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create entrypoint script
RUN echo '#!/bin/bash
PORT="${PORT:-8080}"
echo "Starting server on port: $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]