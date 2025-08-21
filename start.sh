#!/bin/bash

echo "Starting Black-Scholes Option Pricing Application..."
echo "=========================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Start the application
echo "Starting Flask application..."
echo "Access the application at: http://localhost:5001"
python3 app.py
