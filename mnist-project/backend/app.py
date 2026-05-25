from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from io import BytesIO
import base64
from PIL import Image
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MNIST Digit Predictor API",
    description="API for predicting handwritten digits using a CNN model",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

class PredictionRequest(BaseModel):
    image_base64: str

class PredictionResponse(BaseModel):
    digit: int
    confidence: float
    all_confidences: dict

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model
    model_path = os.path.join(os.path.dirname(__file__), '../models/mnist_model.pkl')

    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        logger.info("Please run the training notebook first to generate the model")
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded successfully from {model_path}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

@app.get("/", tags=["Health Check"])
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "MNIST Digit Predictor API",
        "version": "1.0.0"
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Predict digit from a Base64 encoded image

    Args:
        request: Contains Base64 encoded image string

    Returns:
        Prediction with digit, confidence, and all class confidences
    """
    try:
        # Decode Base64 image
        image_data = base64.b64decode(request.image_base64)
        image = Image.open(BytesIO(image_data))

        # Convert to grayscale and resize to 28x28
        image = image.convert('L')
        image = image.resize((28, 28))

        # Convert to numpy array and normalize
        img_array = np.array(image, dtype='float32') / 255.0

        # Reshape for model input (1, 28, 28, 1)
        img_array = np.expand_dims(img_array, axis=(0, -1))

        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        prediction_probs = predictions[0]

        digit = int(np.argmax(prediction_probs))
        confidence = float(np.max(prediction_probs))

        # Create dictionary of all confidences
        all_confidences = {
            str(i): float(prob)
            for i, prob in enumerate(prediction_probs)
        }

        logger.info(f"Prediction: digit={digit}, confidence={confidence:.4f}")

        return PredictionResponse(
            digit=digit,
            confidence=confidence,
            all_confidences=all_confidences
        )

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "service": "MNIST Digit Predictor API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
