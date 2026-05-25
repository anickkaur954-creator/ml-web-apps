import streamlit as st
import requests
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="MNIST Digit Predictor",
    page_icon="🔢",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
    .digit-display {
        font-size: 4rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 1rem 0;
    }
    .confidence-display {
        font-size: 1.2rem;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>🔢 MNIST Digit Predictor</h1>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # API configuration
    api_host = st.text_input(
        "API Host",
        value="http://localhost:8000",
        help="The URL where the FastAPI backend is running"
    )

    st.divider()

    # Instructions
    st.header("📝 Instructions")
    st.markdown("""
    1. Draw a digit (0-9) on the canvas
    2. Make sure the digit fills most of the canvas
    3. Click "🎯 Predict" button
    4. View the prediction result

    **Tips:**
    - Draw slowly and clearly
    - Use a light background, dark foreground
    - The digit should be centered in the canvas
    """)

    st.divider()

    # About
    st.header("ℹ️ About")
    st.markdown("""
    This app uses a Convolutional Neural Network (CNN)
    trained on the MNIST dataset to recognize
    handwritten digits (0-9).

    **Backend:** FastAPI + TensorFlow/Keras
    **Frontend:** Streamlit
    """)

# Main content
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("✏️ Draw a Digit")

    # Check if streamlit-canvas is available
    try:
        from streamlit_canvas import st_canvas

        # Create canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=3,
            stroke_color="rgb(0, 0, 0)",
            background_color="rgb(255, 255, 255)",
            height=280,
            width=280,
            drawing_mode="freedraw",
            key="canvas",
        )

        canvas_image = canvas_result.image_data

    except ImportError:
        st.warning("⚠️ streamlit-canvas is not installed. Please install it using:\n"
                   "`pip install streamlit-canvas`")
        canvas_image = None

with col2:
    st.subheader("🎯 Actions")

    # Predict button
    predict_button = st.button(
        "🎯 Predict",
        key="predict_btn",
        use_container_width=True,
        help="Submit your drawing for prediction"
    )

    st.divider()

    # Clear button
    if st.button("🗑️ Clear Canvas", key="clear_btn", use_container_width=True):
        st.rerun()

    st.divider()

    # Status indicator
    st.subheader("📊 Status")
    status_placeholder = st.empty()

# Prediction section
if predict_button and canvas_image is not None:
    # Convert canvas image to PIL Image
    pil_image = Image.fromarray(canvas_image.astype('uint8'))

    # Convert to grayscale
    pil_image = pil_image.convert('L')

    # Resize to 28x28
    pil_image = pil_image.resize((28, 28))

    # Convert to base64
    buffer = BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    try:
        # Show status
        with status_placeholder.container():
            st.info("⏳ Making prediction...")

        # Send prediction request
        response = requests.post(
            f"{api_host}/predict",
            json={"image_base64": image_base64},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            # Clear status
            status_placeholder.empty()

            # Display results
            st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"<div class='digit-display'>{result['digit']}</div>",
                           unsafe_allow_html=True)

            with col2:
                confidence = result['confidence']
                st.markdown(f"<div class='confidence-display'>"
                           f"Confidence: {confidence:.2%}</div>",
                           unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Display all confidences
            st.subheader("📈 All Predictions")

            # Create a bar chart of all confidences
            confidences = result['all_confidences']
            confidences_dict = {int(k): float(v) for k, v in confidences.items()}
            confidences_dict = dict(sorted(confidences_dict.items()))

            # Display as bar chart
            st.bar_chart(confidences_dict)

            # Display as table
            with st.expander("📋 Detailed Predictions"):
                df_data = {
                    "Digit": list(confidences_dict.keys()),
                    "Confidence": list(confidences_dict.values()),
                    "Percentage": [f"{v:.2%}" for v in confidences_dict.values()]
                }
                st.dataframe(df_data, use_container_width=True)

        else:
            status_placeholder.empty()
            st.error(f"❌ Prediction failed with status code {response.status_code}")
            st.error(response.text)

    except requests.exceptions.ConnectionError:
        status_placeholder.empty()
        st.error(f"❌ Cannot connect to API at {api_host}")
        st.info("Make sure the FastAPI backend is running on the specified host")

    except requests.exceptions.Timeout:
        status_placeholder.empty()
        st.error("❌ Request timeout. The API took too long to respond.")

    except Exception as e:
        status_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")

elif predict_button and canvas_image is None:
    st.warning("⚠️ Please draw something on the canvas first!")
