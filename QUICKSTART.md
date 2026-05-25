# Quick Start Guide

## Setup & Running the Projects

### MNIST Digit Predictor

#### Step 1: Train the Model

```bash
cd mnist-project
cd notebooks

# Install dependencies (if not already installed)
pip install jupyter tensorflow keras numpy

# Start Jupyter and run train_mnist.ipynb
jupyter notebook train_mnist.ipynb
```

Run all cells in the notebook. This will:
- Load the MNIST dataset
- Build and train a CNN model
- Save the model to `../models/mnist_model.pkl`

#### Step 2: Start the Backend API

```bash
cd ../backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Step 3: Start the Frontend (in a new terminal)

```bash
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

#### Step 4: Use the Application

1. Open http://localhost:8501 in your browser
2. Draw a digit (0-9) on the canvas
3. Click "🎯 Predict" button
4. View the prediction result

---

### UFO Sighting Predictor

#### Step 1: Start the Backend API

```bash
cd ufo-project/backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

#### Step 2: Start the Frontend (in a new terminal)

```bash
cd ufo-project/frontend
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

#### Step 3: Use the Application

1. Open http://localhost:8501 in your browser
2. Enter sighting duration in seconds
3. Enter latitude and longitude
4. Click "🔮 Predict" button
5. View the predicted country

---

## Testing the APIs

### MNIST Backend Test

```bash
# Test health check
curl http://localhost:8000/

# Test prediction (requires base64 encoded image)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAAsElEQVR42mNgGAWjYBSMglEwCkYBCWAYGBgYGBkZGRkZGBj+/2dgYPj/n4HhPwMDAwMDA/8/BgaG/wwMDAwM/xkYGBgYGP4zMDBw/P+fgeE/AwPD/wYGhv8MDF//MzD8/8/w/z8Dw3+G/wwM//8zMDwAfzMw/GdgYPhPq4FhFIyCUTAKRsEoGAWjYBSQGBgYGBgZGRkZGRkZGRkYGBj+MzAwMDAwMDAwMDAw/GdgYPjPwMDAwPCfgeE/A8N/BgaG/wwM/xkYGP4z/GeAGDAwMAD0R9NEMPvYTQAAAABJRU5ErkJggg=="}'
```

### UFO Backend Test

```bash
# Test health check
curl http://localhost:8000/

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"seconds": 120, "latitude": 40.7128, "longitude": -74.0060}'
```

---

## Troubleshooting

### Port Already in Use

If you get "Port 8000 already in use" error:

```bash
# For Linux/Mac
lsof -i :8000
kill -9 <PID>

# For Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found

Make sure you've installed dependencies for both frontend and backend:

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

### Streamlit Connection Error

Make sure both services are running:
- Backend should be running on http://localhost:8000
- Frontend will run on http://localhost:8501

Check the API host in the sidebar configuration matches where your backend is running.

---

## API Documentation

### MNIST Backend

**Base URL:** `http://localhost:8000`

#### GET /
Health check endpoint

```bash
curl http://localhost:8000/
```

#### POST /predict
Make a prediction on a handwritten digit

**Request:**
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA..."
}
```

**Response:**
```json
{
  "digit": 7,
  "confidence": 0.9987,
  "all_confidences": {
    "0": 0.0001,
    "1": 0.0002,
    "2": 0.0001,
    ...
    "7": 0.9987,
    ...
  }
}
```

### UFO Backend

**Base URL:** `http://localhost:8000`

#### GET /
Health check endpoint

#### POST /predict
Predict UFO sighting location

**Request:**
```json
{
  "seconds": 120,
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response:**
```json
{
  "country": "US",
  "country_code": 4,
  "confidence": 0.95
}
```

#### GET /countries
Get list of available countries

---

## Architecture Overview

### MNIST Pipeline

```
User Input (Canvas Drawing)
        ↓
Streamlit Frontend (Port 8501)
        ↓ (HTTP POST with Base64 image)
FastAPI Backend (Port 8000)
        ↓ (Decode → Normalize → Preprocess)
TensorFlow CNN Model
        ↓ (Prediction)
Return (Digit + Confidence)
        ↓
Display Result in Streamlit UI
```

### UFO Pipeline

```
User Input (Duration, Lat, Lon)
        ↓
Streamlit Frontend (Port 8501)
        ↓ (HTTP POST with features)
FastAPI Backend (Port 8000)
        ↓ (Prepare features)
scikit-learn Model
        ↓ (Prediction)
Return (Country + Confidence)
        ↓
Display Result in Streamlit UI
```

---

## Project Structure

```
ml-web-apps/
├── mnist-project/
│   ├── notebooks/
│   │   └── train_mnist.ipynb
│   ├── models/
│   │   └── mnist_model.pkl
│   ├── backend/
│   │   ├── app.py
│   │   └── requirements.txt
│   └── frontend/
│       ├── streamlit_app.py
│       └── requirements.txt
│
├── ufo-project/
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── ufo-model.pkl
│   ├── frontend/
│   │   ├── streamlit_app.py
│   │   └── requirements.txt
│   └── data/
│       └── ufos.csv
│
└── README.md
```

---

## Next Steps

- Task 2: Cloud Deployment
- Task 3: Docker Containerization
- MNIST Optimization Challenge

Happy coding! 🚀
