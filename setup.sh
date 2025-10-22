#!/bin/bash

# Setup script for demo-hackerton project
# This script creates a virtual environment and installs dependencies

set -e

echo "======================================"
echo "Setting up demo-hackerton project"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv .venv

echo ""
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Step 4: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "To start the application, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  cd backend && uvicorn main:app --reload"
