FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000
ENV ENVIRONMENT=production

# Command to run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT