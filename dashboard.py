import streamlit as st
import requests

st.set_page_config(
    page_title="AquaSense",
    page_icon="💧",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "parameters" not in st.session_state:
    st.session_state.parameters = {}


# ============================================================
# CUSTOM STYLE
# Native Streamlit only - NO HTML
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #071827;
    }

    /* Main content width */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* General text */
    h1, h2, h3, p, label {
        color: #EAFBFF !important;
    }

    /* AquaSense title */
    h1 {
        color: #39D6E8 !important;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Section headings */
    h2 {
        color: #EAFBFF !important;
        font-weight: 650;
    }

    h3 {
        color: #39D6E8 !important;
    }

    /* Input boxes */
    input {
        background-color: #102536 !important;
        color: #FFFFFF !important;
        border: 1px solid #24566A !important;
    }

    /* Input labels */
    .stTextInput label,
    .stNumberInput label {
        color: #AEEAF2 !important;
        font-weight: 600 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #123B4B;
        color: #FFFFFF;
        border: 1px solid #39D6E8;
        border-radius: 8px;
        font-weight: 650;
        padding: 0.65rem 1rem;
    }

    .stButton > button:hover {
        background-color: #175365;
        border-color: #62E6F3;
        color: #FFFFFF;
    }

    /* Divider */
    hr {
        border-color: #1C4557 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #102536;
        border: 1px solid #24566A;
        border-radius: 10px;
        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #8FDDE8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    /* Success box */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Captions */
    .stCaption {
        color: #79A9B5 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

def show_header():

    st.title("💧 AquaSense")

    st.caption(
        "AI-BASED SMART WATER QUALITY MONITORING SYSTEM"
    )

    st.divider()


# ============================================================
# PROGRESS
# ============================================================

def show_progress():

    st.divider()

    if st.session_state.page == 1:
        st.caption(
            "01 LOGIN   →   02 WATER READINGS   →   03 ANALYSIS"
        )

    elif st.session_state.page == 2:
        st.caption(
            "01 LOGIN   ✓   02 WATER READINGS   →   03 ANALYSIS"
        )

    else:
        st.caption(
            "01 LOGIN   ✓   02 WATER READINGS   ✓   03 ANALYSIS"
        )

    st.caption(
        "AUTHORIZED ACCESS ONLY  •  AQUASENSE"
    )


# ============================================================
# PAGE 1 — LOGIN
# ============================================================

def login_page():

    show_header()

    st.header("🔐 Secure Login")

    st.write(
        "Enter your authorized credentials to access "
        "the water quality monitoring system."
    )

    st.write("")

    username = st.text_input(
        "USERNAME",
        placeholder="Enter your name",
        key="username_input"
    )

    password = st.text_input(
        "PASSWORD",
        type="password",
        placeholder="Enter your password",
        key="password_input"
    )

    st.write("")

    if st.button(
        "LOGIN  →",
        use_container_width=True
    ):

        username_clean = username.strip()

        valid_name = (
            username_clean != ""
            and all(
                character.isalpha() or character.isspace()
                for character in username_clean
            )
        )

        if valid_name and password == "UMIT@123":

            st.session_state.logged_in = True
            st.session_state.username = username_clean
            st.session_state.page = 2

            st.rerun()

        elif not valid_name:

            st.error(
                "Please enter a valid name using letters and spaces only."
            )

        else:

            st.error("Incorrect password.")

    if st.button(
        "Forgot Password?",
        use_container_width=True
    ):

        st.info(
            "Password Reset: Please contact the system administrator "
            "to reset or verify your access password."
        )

    show_progress()


# ============================================================
# PAGE 2 — WATER READINGS
# ============================================================

def input_page():

    show_header()

    st.header("💧 Water Quality Input")

    st.write(
        f"Welcome, {st.session_state.username}. "
        "Enter the sensor readings from the water sample."
    )

    st.write("")

    # Main section
    st.subheader("WATER PARAMETERS")

    st.caption(
        "Provide the four measured parameters for AI-based analysis."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=7.0,
            step=0.1,
            key="ph_input"
        )

        tds = st.number_input(
            "TDS (ppm)",
            min_value=0.0,
            value=300.0,
            step=1.0,
            key="tds_input"
        )

    with col2:

        turbidity = st.number_input(
            "Turbidity (NTU)",
            min_value=0.0,
            value=2.0,
            step=0.1,
            key="turbidity_input"
        )

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            value=25.0,
            step=0.1,
            key="temperature_input"
        )

    st.write("")

    st.info(
        "The AI model will analyze pH, TDS, turbidity and temperature "
        "to classify the water sample."
    )

    st.write("")

    if st.button(
        "🔍  ANALYZE WATER QUALITY",
        use_container_width=True
    ):

        data = {
            "pH": ph,
            "TDS_ppm": tds,
            "Turbidity_NTU": turbidity,
            "Temperature_C": temperature
        }

        try:

            response = requests.post(
                "http://127.0.0.1:5000/predict",
                json=data,
                timeout=10
            )

            if response.status_code == 200:

                result = response.json()

                st.session_state.prediction = result["prediction"]

                st.session_state.parameters = data

                st.session_state.page = 3

                st.rerun()

            else:

                try:
                    error_message = response.json().get(
                        "error",
                        "Unknown error"
                    )

                except Exception:
                    error_message = "Unknown error"

                st.error(
                    f"Prediction error: {error_message}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Flask API is not running. "
                "Please start app.py first."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        except Exception as error:

            st.error(
                f"An error occurred: {error}"
            )

    show_progress()


# ============================================================
# PAGE 3 — ANALYSIS
# ============================================================

def result_page():

    show_header()

    prediction = st.session_state.prediction

    parameters = st.session_state.parameters

    st.header("📊 Water Quality Analysis")

    st.write(
        "AI-generated assessment of the submitted water sample."
    )

    st.write("")

    # --------------------------------------------------------
    # LARGE RESULT
    # --------------------------------------------------------

    st.subheader("AI WATER QUALITY ASSESSMENT")

    if prediction.lower() == "safe":

        st.success(
            "## ✓  WATER IS SAFE"
        )

        st.write(
            "The analyzed water sample has been classified "
            "as SAFE by the AI model."
        )

    else:

        st.error(
            "## ⚠  WATER IS UNSAFE"
        )

        st.write(
            "The analyzed water sample has been classified "
            "as UNSAFE by the AI model."
        )

    st.write("")

    st.divider()

    # --------------------------------------------------------
    # PARAMETERS
    # --------------------------------------------------------

    st.subheader("MEASURED WATER PARAMETERS")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "pH",
            f'{parameters["pH"]:.1f}'
        )

    with col2:

        st.metric(
            "TDS",
            f'{parameters["TDS_ppm"]:.1f} ppm'
        )

    with col3:

        st.metric(
            "Turbidity",
            f'{parameters["Turbidity_NTU"]:.1f} NTU'
        )

    with col4:

        st.metric(
            "Temperature",
            f'{parameters["Temperature_C"]:.1f} °C'
        )

    st.write("")

    st.divider()

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    st.subheader("RECOMMENDATION")

    if prediction.lower() == "safe":

        st.success(
            "✓ The analyzed sample has been classified as SAFE "
            "according to the trained AI model.\n\n"
            "Continue regular monitoring of the water quality "
            "to maintain consistent water safety."
        )

    else:

        st.warning(
            "⚠ The analyzed sample has been classified as UNSAFE "
            "according to the trained AI model.\n\n"
            "The water should be further tested and appropriate "
            "treatment or corrective measures should be considered "
            "before use."
        )

    st.write("")

    if st.button(
        "↻  ANALYZE ANOTHER SAMPLE",
        use_container_width=True
    ):

        st.session_state.prediction = None

        st.session_state.parameters = {}

        st.session_state.page = 2

        st.rerun()

    show_progress()


# ============================================================
# PAGE CONTROL
# ============================================================

if not st.session_state.logged_in:

    login_page()

elif st.session_state.page == 2:

    input_page()

elif st.session_state.page == 3:

    result_page()

else:

    login_page()