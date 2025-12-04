import streamlit as st
from core.pipeline import run_rippletruth_pipeline

st.set_page_config(page_title="RippleTruth Analyzer", layout="wide")

st.title("🌀 RippleTruth — Intention & Origin Analyzer")
st.write("Paste text below to run the RippleTruth pipeline.")

text = st.text_area("Input Text", height=200)

if st.button("Analyze"):
    if not text.strip():
        st.error("Please enter text to analyze.")
    else:
        result = run_rippletruth_pipeline(text)
        st.subheader("📘 Markdown Output")
        st.markdown(result["markdown"], unsafe_allow_html=True)
