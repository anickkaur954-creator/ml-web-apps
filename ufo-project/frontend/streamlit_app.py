import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="UFO Sighting Predictor",
    page_icon="👽",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2d3436;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
    .country-display {
        font-size: 3rem;
        font-weight: bold;
        color: #27ae60;
        margin: 1rem 0;
    }
    .confidence-display {
        font-size: 1.2rem;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>👽 UFO Sighting Predictor</h1>", unsafe_allow_html=True)

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
    1. Enter the UFO sighting duration (in seconds)
    2. Enter the geographical location (latitude and longitude)
    3. Click "🔮 Predict" button
    4. View the predicted country

    **Tips:**
    - Duration: 0 to 1440 seconds (24 hours)
    - Latitude: -90 to 90 (South to North)
    - Longitude: -180 to 180 (West to East)

    **Example Coordinates:**
    - New York: 40.7128, -74.0060
    - London: 51.5074, -0.1278
    - Sydney: -33.8688, 151.2093
    - Toronto: 43.6532, -79.3832
    - Berlin: 52.5200, 13.4050
    """)

    st.divider()

    # About
    st.header("ℹ️ About")
    st.markdown("""
    This app uses a machine learning classifier
    to predict the likely country of a UFO sighting
    based on duration and location.

    **Backend:** FastAPI + scikit-learn
    **Frontend:** Streamlit
    **Model:** Random Forest or similar
    """)

# Main content
st.subheader("🛸 Enter UFO Sighting Details")

col1, col2 = st.columns(2)

with col1:
    seconds = st.number_input(
        "Duration (seconds)",
        min_value=0,
        max_value=1440,
        value=60,
        step=1,
        help="How long was the UFO sighting in seconds?"
    )

with col2:
    latitude = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=40.7128,
        step=0.0001,
        format="%.4f",
        help="Geographic latitude of sighting location"
    )

longitude = st.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=-74.0060,
    step=0.0001,
    format="%.4f",
    help="Geographic longitude of sighting location"
)

st.divider()

# Prediction section
col1, col2, col3 = st.columns(3)

with col1:
    predict_button = st.button(
        "🔮 Predict",
        key="predict_btn",
        use_container_width=True,
        help="Submit your sighting details for prediction"
    )

with col2:
    reset_button = st.button(
        "🔄 Reset",
        key="reset_btn",
        use_container_width=True,
        help="Reset form to default values"
    )

with col3:
    pass  # Placeholder for alignment

# Handle reset
if reset_button:
    st.rerun()

# Prediction
if predict_button:
    status_placeholder = st.empty()

    try:
        # Show status
        with status_placeholder.container():
            st.info("⏳ Making prediction...")

        # Prepare request
        payload = {
            "seconds": int(seconds),
            "latitude": float(latitude),
            "longitude": float(longitude)
        }

        # Send prediction request
        response = requests.post(
            f"{api_host}/predict",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            # Clear status
            status_placeholder.empty()

            # Display results
            st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)

            st.markdown(f"<div class='country-display'>{result['country']}</div>",
                       unsafe_allow_html=True)

            confidence = result['confidence']
            st.markdown(f"<div class='confidence-display'>"
                       f"Confidence: {confidence:.2%}</div>",
                       unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Display detailed information
            st.subheader("📊 Prediction Details")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Predicted Country",
                    result['country'],
                    help="The predicted country of the sighting"
                )

            with col2:
                st.metric(
                    "Country Code",
                    int(result['country_code']),
                    help="Internal country code (0-4)"
                )

            with col3:
                st.metric(
                    "Confidence Score",
                    f"{confidence:.2%}",
                    help="Model's confidence in the prediction"
                )

            # Display input summary
            st.divider()
            st.subheader("📍 Input Summary")

            summary_data = {
                "Duration": f"{int(seconds)} seconds",
                "Latitude": f"{latitude:.4f}",
                "Longitude": f"{longitude:.4f}",
                "API Endpoint": f"{api_host}/predict"
            }

            for key, value in summary_data.items():
                st.write(f"**{key}:** {value}")

        else:
            status_placeholder.empty()
            st.error(f"❌ Prediction failed with status code {response.status_code}")

            try:
                error_details = response.json()
                st.error(json.dumps(error_details, indent=2))
            except:
                st.error(response.text)

    except requests.exceptions.ConnectionError:
        status_placeholder.empty()
        st.error(f"❌ Cannot connect to API at {api_host}")
        st.info("ℹ️ Make sure the FastAPI backend is running:")
        st.code("cd backend && uvicorn app:app --reload --port 8000", language="bash")

    except requests.exceptions.Timeout:
        status_placeholder.empty()
        st.error("❌ Request timeout. The API took too long to respond.")

    except Exception as e:
        status_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
---
**UFO Sighting Predictor** | Created with ❤️ using Streamlit and FastAPI
""")
