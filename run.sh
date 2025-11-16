#!/bin/bash

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     VigilantAI - System Dashboard      ║"
echo "║     Starting Backend Server...         ║"
echo "╚════════════════════════════════════════╝"
echo ""

cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     Server starting on:                ║"
echo "║     http://localhost:8000              ║"
echo "║                                        ║"
echo "║  Demo Credentials:                     ║"
echo "║  Username: admin                       ║"
echo "║  Password: admin                       ║"
echo "║                                        ║"
echo "║  Press Ctrl+C to stop the server       ║"
echo "╚════════════════════════════════════════╝"
echo ""

python main.py
