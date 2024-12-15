#!/bin/sh

# Debug information
echo "Environment variables:"
env

# Handle PORT with explicit fallback
if [ -z "$PORT" ]; then
    echo "PORT not set, using default 8080"
    export PORT=8080
fi

echo "Using PORT: $PORT"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
