FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure script is executable
RUN chmod +x start.sh

# Default port (will be overridden by Railway)
ENV PORT=8080

# Use shell form for CMD to ensure proper variable expansion
CMD ./start.sh