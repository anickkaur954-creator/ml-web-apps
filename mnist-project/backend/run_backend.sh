#!/bin/bash
# Start MNIST FastAPI Backend

echo "=========================================="
echo "  MNIST FastAPI Backend Startup"
echo "=========================================="
echo ""

# Check if model exists
if [ ! -f "./models/mnist_model.pkl" ]; then
    echo "❌ ERROR: Model file not found at ./models/mnist_model.pkl"
    echo ""
    echo "Please run train_model.py first:"
    echo "  python train_model.py"
    exit 1
fi

echo "✅ Model file found"
echo ""
echo "Starting FastAPI backend on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

uvicorn app:app --reload --port 8000 --host 0.0.0.0
