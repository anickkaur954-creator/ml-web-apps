#!/bin/bash
# Start MNIST Streamlit Frontend

echo "=========================================="
echo "  MNIST Streamlit Frontend Startup"
echo "=========================================="
echo ""

echo "✅ Starting Streamlit frontend on http://localhost:8501"
echo ""
echo "Make sure the FastAPI backend is running on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

streamlit run streamlit_app.py --server.port 8501 --logger.level=info
