#!/usr/bin/env python3
"""
Quick MNIST model training script
Trains a CNN model and saves it as pickle for the FastAPI backend
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import pickle
import os
import sys

print("=" * 60)
print("MNIST Model Training Script")
print("=" * 60)

# Step 1: Load data
print("\n[1/4] Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(f"Training data shape: {x_train.shape}")
print(f"Test data shape: {x_test.shape}")

# Step 2: Prepare data
print("\n[2/4] Preparing data...")
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
print("Data normalization and reshaping complete")

# Step 3: Build and train model
print("\n[3/4] Building and training CNN model...")
model = keras.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"Model parameters: {model.count_params():,}")
print("\nTraining model (this may take a few minutes)...")

history = model.fit(
    x_train, y_train,
    batch_size=128,
    epochs=10,
    validation_split=0.1,
    verbose=1
)

# Step 4: Evaluate and save
print("\n[4/4] Evaluating and saving model...")
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Create models directory if needed
models_dir = './models'
os.makedirs(models_dir, exist_ok=True)

# Save model as pickle
model_path = os.path.join(models_dir, 'mnist_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

model_size = os.path.getsize(model_path) / 1024 / 1024
print(f"\n✅ Model saved to: {model_path}")
print(f"   File size: {model_size:.2f} MB")

print("\n" + "=" * 60)
print("Training complete! Model is ready for the FastAPI backend.")
print("=" * 60)
