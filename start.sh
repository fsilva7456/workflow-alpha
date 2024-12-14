#!/bin/bash

# Print environment variables for debugging
echo "Environment variables:"
echo "PORT: $PORT"
echo "ENVIRONMENT: $ENVIRONMENT"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1