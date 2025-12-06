import sys
import os

# Ensure project directory is on the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

from utils.input_resolver import resolve_input
from core.pipeline import run_rippletruth_pipeline
from core.human_narrative_layer import human_narrative_summary
from core.ai_engine import run_ai_enhancement


# --------------------------------------------------------
# PAGE SETUP
# --------------------------------------------------------
st.set_page_config(page_title="RippleTruth", layout="wide")

st.markdown(
    """
    <style>
        body { font-family: 'Roboto', sans-serif; }

        .metric-table td, .metric-table th {
            padding: 6px 12px !important;
            text-align: left !important;
        }

        .metric-tooltip {
            color: #AAA;
            cursor: help;
            padding-left: 6px;
        }

        .value-green { color: #5CFF8F !important; font-weight: 600; }
        .value-yellow { color: #FFD447 !important; font-weight: 600; }
        .value-red { color: #FF6B6B !important; font-weight: 600; }
        .value-blue { color: #6EC6FF !important; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("RippleTruth — Intention-Based Traceback Analyzer")
st.caption(
    "Upload text, images, or URLs and generate an AI-enhanced RippleTruth Intelligence Report using "
    "RippleScan + Intention Math + Traceback + Human Mode + AI Expansion."
)


# --------------------------------------------------------
# OPTIONAL OPENAI KEY
# --------------------------------------------------------
with st.expander("🔑 Optional: Add OpenAI API Key for AI Enhancements"):
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    st.caption("AI enhancements remain disabled unless a valid key is entered.")


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
# CLEAN ARTICLE SCRAPER
# --------------------------------------------------------
def extract_clean_article(url: str) -> str:
    """Lightweight, Streamlit-safe article extraction."""
    try:
        resp = requests.get(url, timeout=10)
    except:
        return "[Error: Could not retrieve URL]"

    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text_blocks = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 40]

    if not text_blocks:
        return "[No readable article text found]"

    return "\n\n".join(text_blocks)


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

    if input_type == "URL" and url_value:
        st.info("Extracting clean article text from URL…")
        clean_text = extract_clean_article(url_value)
        if clean_text.startswith("[Error") or clean_text.startswith("[No readable"):
            st.error(clean_text)
            st.stop()
        resolved["text"] = clean_text

    if resolved["source_type"] is None:
        st.error("No input provided.")
        st.stop()

    text = resolved["text"]

    if text.startswith("[Error") or text.startswith("[No readable"):
        st.error(text)
        st.stop()

    # --------------------------------------------------------
    # RUN PIPELINE
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
    # INTENTION FIELD METRICS TABLE (FIXED VERSION)
    # --------------------------------------------------------
    st.subheader("🔬 Intention Field Metrics")

    def colorize(value):
        if value < 0.15:
            return f"<span class='value-green'>{value:.4f}</span>"
        if value < 0.35:
            return f"<span class='value-yellow'>{value:.4f}</span>"
        if value < 0.55:
            return f"<span class='value-blue'>{value:.4f}</span>"
        return f"<span class='value-red'>{value:.4f}</span>"

    table_html = f"""
<table class="metric-table">
<tr><th>Metric</th><th>Value</th></tr>

<tr>
<td>FILS <span class='metric-tooltip' title='Forward Intention Likelihood Score — How primed the narrative is to spread.'>ⓘ</span></td>
<td>{colorize(intention['FILS'])}</td>
</tr>

<tr>
<td>UCIP <span class='metric-tooltip' title='Unified Intention Field Scalar — Measures coherence and structural force.'>ⓘ</span></td>
<td>{colorize(intention['UCIP'])}</td>
</tr>

<tr>
<td>TTCF <span class='metric-tooltip' title='Chaos Factor — Measures volatility and mutation potential.'>ⓘ</span></td>
<td>{colorize(intention['TTCF'])}</td>
</tr>

<tr>
<td>Drift <span class='metric-tooltip' title='Alignment Shift — Measures narrative wobble over time.'>ⓘ</span></td>
<td>{colorize(intention['Drift'])}</td>
</tr>

<tr>
<td>RippleScore <span class='metric-tooltip' title='Composite Stability Index — Overall signal cohesion and strength.'>ⓘ</span></td>
<td>{colorize(intention['RippleScore'])}</td>
</tr>

</table>
"""

    st.markdown(table_html, unsafe_allow_html=True)

    # --------------------------------------------------------
    # EXPANDED DEEP DIVE
    # --------------------------------------------------------
    with st.expander("📘 Deep Dive: Understanding the Intention Metrics"):
        st.markdown(
            """
### **FILS — Forward Intention Likelihood Score**  
Likelihood a narrative is primed to spread or escalate.  
Low FILS means the message will likely fade; high FILS means it can mobilize or travel quickly.

### **UCIP — Unified Intention Field Scalar**  
Measures coherence, density, and structural force inside the intention field.  
High UCIP suggests coordinated framing or strong emotional anchor.

### **TTCF — Chaos Factor**  
Reflects instability, unpredictability, and mutation potential.  
High TTCF means the narrative environment is volatile or rumor-driven.

### **Drift — Alignment Shift**  
Represents wobble or direction change in intention over time.  
High drift means the narrative is being reframed or evolving fast.

### **RippleScore — Composite Stability Index**  
Blends all metrics into one overall coherence + stability score.  
Low = fragmented, emerging narrative.  
High = structured, stable narrative environment.
"""
        )

    # --------------------------------------------------------
    # TRACEBACK / ORIGIN
    # --------------------------------------------------------
    st.subheader("🛰️ Traceback / Origin Analysis")

    origin_label = trace.get("origin_label", "general – low signal origin")
    origin_conf = trace.get("origin_confidence", 0.0)

    st.markdown(f"**Origin Assessment:** {origin_label}  \n**Confidence:** {origin_conf:.3f}")
    st.markdown(f"**Amplification Pattern:** {trace['amplification_pattern']:.3f}")
    st.markdown(f"**Mutation Likelihood:** {trace['mutation_likelihood']:.3f}")
    st.markdown(f"**RippleTruth Index:** {trace['RippleTruthIndex']:.1f} / 100")

    # --------------------------------------------------------
    # HUMAN NARRATIVE LAYER
    # --------------------------------------------------------
    st.subheader("🧠 Human Narrative Assessment")
    st.markdown(human_narrative_summary(text, intention))

    # --------------------------------------------------------
    # OPTIONAL AI OUTPUT
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
    # ORIGINAL INTERPRETATION
    # --------------------------------------------------------
    st.subheader("🧩 RippleTruth Interpretation")

    if interpretation_text.strip():
        st.markdown(interpretation_text)
    else:
        st.markdown("_(No interpretation returned.)_")
