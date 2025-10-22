#!/bin/bash

# Run script for demo-hackerton project
# This script activates the virtual environment and starts the FastAPI server

set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

echo "======================================"
echo "Starting demo-hackerton application"
echo "======================================"
echo ""

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting FastAPI server..."
echo ""
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
