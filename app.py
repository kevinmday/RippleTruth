import sys
import os

# Ensure project directory is on the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from utils.input_resolver import resolve_input
from core.pipeline import run_rippletruth_pipeline
from core.human_narrative_layer import human_narrative_summary
from core.ai_engine import run_ai_enhancement   # NEW AI MODULE


# --------------------------------------------------------
# PAGE SETUP
# --------------------------------------------------------
st.set_page_config(page_title="RippleTruth", layout="wide")

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
st.caption("Upload text, images, or URLs and generate an AI-enhanced RippleTruth Intelligence Report using RippleScan + Intention Math + Traceback + Human Mode + AI Expansion.")


# --------------------------------------------------------
# OPTIONAL OPENAI KEY
# --------------------------------------------------------
with st.expander("🔑 Optional: Add OpenAI API Key for AI Enhancements"):
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    st.caption("AI enhancements will remain disabled unless a valid key is entered.")


# --------------------------------------------------------
# AI OUTPUT MODE
# --------------------------------------------------------
ai_mode = st.selectbox(
    "Select AI Output Mode:",
    [
        "None (Math + Human Mode Only)",
        "Narrative Summary",
        "Counter-Narrative",
        "Expanded Intelligence Brief",
        "Executive Summary"
    ]
)


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
# Utility: Load image from URL
# --------------------------------------------------------
def fetch_image_from_url(url):
    try:
        resp = requests.get(url)
        return Image.open(BytesIO(resp.content))
    except:
        return None


# --------------------------------------------------------
# PROCESS BUTTON
# --------------------------------------------------------
run_button = st.button("Run RippleTruth Analysis")

if run_button:
    st.markdown("---")
    st.header("RippleTruth Report")

    # --------------------------------------------------------
    # UNIFIED INPUT RESOLUTION
    # --------------------------------------------------------
    resolved = resolve_input(
        text_input=user_text,
        url_input=url_value,
        image_upload=uploaded_image
    )

    if resolved["source_type"] is None:
        st.error("No input provided.")
        st.stop()

    if resolved["text"].startswith("[Error") or resolved["text"].startswith("[No readable"):
        st.error(resolved["text"])
        st.stop()

    text = resolved["text"]

    # --------------------------------------------------------
    # RUN CORE RIPPLETRUTH PIPELINE
    # --------------------------------------------------------
    output = run_rippletruth_pipeline(text)

    narrative = output["narrative"]
    intention = output["intention"]
    trace = output["traceback"]
    interpretation_text = output["interpretation"]

    # --------------------------------------------------------
    # NARRATIVE SUMMARY
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
    # TRACEBACK / ORIGIN
    # --------------------------------------------------------
    st.subheader("🛰️ Traceback / Origin Analysis")

    origin_label = trace.get("origin_label", "general – low signal origin")
    origin_conf = trace.get("origin_confidence", 0.0)

    amp = round(trace["amplification_pattern"], 3)
    mut = round(trace["mutation_likelihood"], 3)
    rti = round(trace["RippleTruthIndex"], 1)

    st.markdown(f"**Origin Assessment:** {origin_label}  \n**Confidence:** {origin_conf:.3f}")
    st.markdown(f"**Amplification Pattern:** {amp}")
    st.markdown(f"**Mutation Likelihood:** {mut}")
    st.markdown(f"**RippleTruth Index:** {rti} / 100")


    # --------------------------------------------------------
    # HUMAN NARRATIVE LAYER (ALWAYS INCLUDED)
    # --------------------------------------------------------
    st.subheader("🧠 Human Narrative Assessment")

    human_summary = human_narrative_summary(text, intention)
    st.markdown(human_summary)


    # --------------------------------------------------------
    # AI ENHANCEMENT (OPTIONAL)
    # --------------------------------------------------------
    if ai_mode != "None (Math + Human Mode Only)" and not api_key:
        st.warning("AI mode selected but no API key entered.")
    elif api_key and ai_mode != "None (Math + Human Mode Only)":
        st.subheader("🤖 AI-Enhanced Output")

        ai_output = run_ai_enhancement(
            text=text,
            narrative=narrative,
            intention=intention,
            traceback=trace,
            mode=ai_mode,
            api_key=api_key
        )

        st.markdown(ai_output)


    # --------------------------------------------------------
    # ORIGINAL INTERPRETATION ENGINE OUTPUT
    # --------------------------------------------------------
    st.subheader("🧩 RippleTruth Interpretation")

    st.markdown(
        interpretation_text
        if interpretation_text.strip()
        else "_(No interpretation returned.)_"
    )
