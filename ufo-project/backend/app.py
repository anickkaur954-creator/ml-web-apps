from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="UFO Sighting Predictor API",
    description="API for predicting UFO sighting locations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Country mapping
COUNTRIES = ["Australia", "Canada", "Germany", "UK", "US"]

# Global model variable
model = None

class UFOPredictionRequest(BaseModel):
    """Request model for UFO prediction"""
    seconds: int = Field(..., ge=0, le=1440, description="Duration in seconds (0-1440)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")

class UFOPredictionResponse(BaseModel):
    """Response model for UFO prediction"""
    country: str
    country_code: int
    confidence: float

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model
    model_path = os.path.join(os.path.dirname(__file__), 'ufo-model.pkl')

    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
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
        "service": "UFO Sighting Predictor API",
        "version": "1.0.0"
    }

@app.post("/predict", response_model=UFOPredictionResponse, tags=["Prediction"])
async def predict(request: UFOPredictionRequest):
    """
    Predict UFO sighting location

    Args:
        request: Contains duration (seconds), latitude, and longitude

    Returns:
        Prediction with country name and confidence
    """
    try:
        # Prepare features in the same format as the original Flask app
        features = np.array([[request.seconds, request.latitude, request.longitude]])

        # Make prediction
        prediction = model.predict(features)[0]

        # Get confidence from the model if available
        try:
            probabilities = model.predict_proba(features)[0]
            confidence = float(np.max(probabilities))
        except AttributeError:
            # If model doesn't have predict_proba, use a default confidence
            confidence = 1.0

        country = COUNTRIES[prediction]

        logger.info(f"Prediction: country={country}, code={prediction}, confidence={confidence:.4f}")

        return UFOPredictionResponse(
            country=country,
            country_code=int(prediction),
            confidence=confidence
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
        "service": "UFO Sighting Predictor API",
        "available_countries": COUNTRIES
    }

@app.get("/countries", tags=["Info"])
async def get_countries():
    """Get list of available countries"""
    return {
        "countries": COUNTRIES,
        "count": len(COUNTRIES)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
