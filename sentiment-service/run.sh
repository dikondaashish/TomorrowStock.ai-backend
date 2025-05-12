#!/bin/bash
# Activate virtual environment if not already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check for port argument
PORT=${1:-8001}

# Start the service with reload for development
echo "Starting Sentiment Service on port $PORT"
uvicorn main:app --reload --host 0.0.0.0 --port $PORT
