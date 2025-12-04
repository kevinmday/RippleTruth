import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from core.pipeline import run_rippletruth_pipeline

st.set_page_config(page_title="RippleTruth", layout="wide")

# --------------------------------------------------------
# GLOBAL STYLE
# --------------------------------------------------------
st.markdown(
    """
    <style>
        body { font-family: 'Roboto', sans-serif; }
        .stTextInput, .stTextArea {
            font-family: 'Roboto Mono', monospace !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("RippleTruth — Intention-Based Traceback Analyzer")
st.caption("Upload text, images, or URLs and generate a RippleTruth Analysis Report using RippleScan + Intention Math + Traceback.")

# --------------------------------------------------------
# INPUT SELECTION
# --------------------------------------------------------
input_type = st.radio(
    "Select Input Type:",
    ["Text", "Image", "URL"],
    horizontal=True,
    label_visibility="collapsed",
)

user_text = None
uploaded_image = None
url_value = None

if input_type == "Text":
    user_text = st.text_area("Paste text here:", height=220)

elif input_type == "Image":
    uploaded_image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

elif input_type == "URL":
    url_value = st.text_input("Enter URL:")


# --------------------------------------------------------
# UTILITY: LOAD IMAGE FROM URL
# --------------------------------------------------------
def fetch_image_from_url(url):
    try:
        resp = requests.get(url)
        return Image.open(BytesIO(resp.content))
    except:
        return None


# --------------------------------------------------------
# PROCESS
# --------------------------------------------------------
run_button = st.button("Run RippleTruth Analysis")

if run_button:
    st.markdown("---")
    st.header("RippleTruth Report")

    # Determine actual text source
    if user_text:
        text = user_text
    elif uploaded_image:
        text = "Image uploaded (OCR not yet applied)"
    elif url_value:
        text = f"URL submitted for analysis: {url_value}"
    else:
        st.error("No valid input provided.")
        st.stop()

    # --------------------------------------------------------
    # RUN MASTER PIPELINE
    # --------------------------------------------------------
    output = run_rippletruth_pipeline(text)

    narrative = output["narrative"]
    intention = output["intention"]
    trace = output["traceback"]

    # --------------------------------------------------------
    # NARRATIVE SECTION
    # --------------------------------------------------------
    st.subheader("🧩 Narrative Summary (RippleScan Lite)")
    st.markdown(
        f"""
        **Topic:** {narrative['topic']}  
        **Polarity:** {narrative['polarity']}  
        **Emotional Tone:** {narrative['tone']}  
        **Structure:** {narrative['structure']}  
        """
    )

    # --------------------------------------------------------
    # INTENTION FIELD METRICS
    # --------------------------------------------------------
    st.subheader("🔬 Intention Field Metrics")

    st.table({
        "Metric": ["FILS", "UCIP", "TTCF", "Drift", "RippleScore"],
        "Value": [
            intention["FILS"],
            intention["UCIP"],
            intention["TTCF"],
            intention["Drift"],
            intention["RippleScore"],
        ]
    })

    # --------------------------------------------------------
    # TRACEBACK ANALYSIS
    # --------------------------------------------------------
    st.subheader("🛰️ Traceback / Origin Analysis")

    # Top actor
    actor_probs = trace["actor_probabilities"]
    dominant_actor = max(actor_probs, key=actor_probs.get)

    st.markdown(f"**Origin Probability (Top Actor):** {dominant_actor}")

    st.markdown(f"**Amplification Pattern:** {round(trace['amplification_pattern'], 3)}")
    st.markdown(f"**Mutation Likelihood:** {round(trace['mutation_likelihood'], 3)}")
    st.markdown(f"**RippleTruth Index:** {round(trace['RippleTruthIndex'], 1)} / 100")

    st.markdown("### Interpretation:")
    st.markdown(trace["interpretation"])

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------
    st.subheader("🧠 RippleTruth Interpretation")
    st.markdown(
        """
        This result integrates:

        - RippleScan narrative extraction  
        - Intention-field analysis (FILS, UCIP, TTCF, Drift, RippleScore)  
        - Traceback origin probability engine  
        - Actor modeling + amplification dynamics  
        - Reliability scoring through the RippleTruth Index  
        """
    )
