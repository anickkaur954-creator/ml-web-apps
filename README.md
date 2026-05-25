# ML Web Apps - MNIST & UFO Predictors

Complete end-to-end machine learning web applications featuring local deployment, cloud migration, and containerization.

## 📚 Projects Overview

### 1. MNIST Digit Predictor
A real-time handwritten digit recognition application built with Streamlit frontend and FastAPI backend.

**Features:**
- Interactive canvas drawing interface
- Real-time digit prediction (0-9)
- Confidence score display
- CNN-based deep learning model

**Tech Stack:** FastAPI, Streamlit, TensorFlow/Keras, scikit-learn

### 2. UFO Sighting Predictor
Predict UFO sighting locations based on duration and geographical coordinates.

**Features:**
- Input-based prediction interface
- Country-level classification
- Simple and intuitive UI
- Production-ready model

**Tech Stack:** FastAPI, Streamlit, scikit-learn, pandas

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### MNIST Project Setup

```bash
cd mnist-project

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Train model and run backend
uvicorn app:app --reload --port 8000

# In another terminal, run frontend
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

Visit: http://localhost:8501

### UFO Project Setup

```bash
cd ufo-project

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run backend
uvicorn app:app --reload --port 8000

# In another terminal, run frontend
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
```

Visit: http://localhost:8501

---

## 📂 Project Structure

```
ml-web-apps/
├── mnist-project/
│   ├── notebooks/
│   │   └── train_mnist.ipynb      # Model training notebook
│   ├── models/
│   │   └── mnist_model.pkl        # Trained model (generated)
│   ├── backend/
│   │   ├── app.py                 # FastAPI application
│   │   └── requirements.txt       # Dependencies
│   └── frontend/
│       ├── streamlit_app.py       # Streamlit UI
│       └── requirements.txt       # Dependencies
│
├── ufo-project/
│   ├── backend/
│   │   ├── app.py                 # FastAPI application
│   │   ├── requirements.txt       # Dependencies
│   │   └── ufo-model.pkl          # Pre-trained model
│   ├── frontend/
│   │   ├── streamlit_app.py       # Streamlit UI
│   │   └── requirements.txt       # Dependencies
│   └── data/
│       └── ufos.csv               # UFO sightings dataset
│
├── docs/                          # Documentation
└── README.md
```

---

## 🎯 Learning Roadmap

### Task 1: Local Deployment ✅
- [x] Project setup and directory structure
- [ ] MNIST model training
- [ ] MNIST backend API
- [ ] MNIST Streamlit frontend
- [ ] UFO FastAPI migration (from Flask)
- [ ] UFO Streamlit frontend
- [ ] Local testing and integration

### Task 2: Cloud Deployment (Coming Soon)
- Cloud VM setup and configuration
- FastAPI backend deployment
- Streamlit frontend deployment
- Production environment setup

### Task 3: Containerization (Coming Soon)
- Docker image creation
- Docker Compose setup
- Container orchestration

---

## 🔧 Configuration

### MNIST Backend (port 8000)
```python
# Expected API endpoints
GET  /              # Health check
POST /predict       # Accept Base64 image, return prediction
```

### UFO Backend (port 8000)
```python
# Expected API endpoints
GET  /              # Health check
POST /predict       # Accept seconds, latitude, longitude
```

---

## 📊 Model Details

### MNIST CNN Model
- **Input:** 28x28 grayscale images
- **Output:** Digit prediction (0-9) with confidence
- **Architecture:** Convolutional Neural Network
- **Framework:** TensorFlow/Keras

### UFO Classification Model
- **Input:** seconds (int), latitude (float), longitude (float)
- **Output:** Country prediction (Australia, Canada, Germany, UK, USA)
- **Framework:** scikit-learn
- **Algorithm:** Random Forest or similar

---

## 🤝 Contributing

Feel free to enhance these projects by:
- Improving model accuracy
- Adding new features
- Optimizing performance
- Writing tests

---

## 📝 License

MIT License - feel free to use this project for learning and development.

---

## 🎓 Learning Resources

- [Bilibili Video Tutorial Series](https://space.bilibili.com/472463946/lists/211561?type=season)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [TensorFlow MNIST Tutorial](https://www.tensorflow.org/datasets/keras_example)

---

## 📞 Support

For questions or issues, please refer to the documentation or create an issue on GitHub.

Last Updated: 2026-05-25
