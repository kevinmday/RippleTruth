# ----------------------------------------------------
# LOCAL IMPORTS — correct paths
# ----------------------------------------------------
import streamlit as st
from utils.url_loader import load_url_text
from core.ocr_engine import extract_text_from_image


def resolve_input(text_input=None, url_input=None, image_upload=None):
    """
    Unified input resolver for RippleTruth.

    Normalizes all three input types and returns a dict with:
      • text          → final resolved text string
      • source_type   → "text", "url", or "image"
      • warnings      → list of warning messages

    This function is SAFE: all three arguments are optional.
    """

    warnings = []

    # ----------------------------------------------------
    # 1) RAW TEXT INPUT
    # ----------------------------------------------------
    if text_input and isinstance(text_input, str) and text_input.strip():
        return {
            "text": text_input.strip(),
            "source_type": "text",
            "warnings": warnings
        }

    # ----------------------------------------------------
    # 2) URL INPUT → FETCH TEXT
    # ----------------------------------------------------
    if url_input and isinstance(url_input, str) and url_input.strip():
        cleaned_url = url_input.strip()
        text = load_url_text(cleaned_url)

        if text.startswith("[") and "Error" in text:
            warnings.append("URL returned an error. See message in preview.")

        return {
            "text": text,
            "source_type": "url",
            "warnings": warnings
        }

    # ----------------------------------------------------
    # 3) IMAGE UPLOAD → OCR
    # ----------------------------------------------------
    if image_upload is not None:
        # OCR always returns a string (success or error string)
        text = extract_text_from_image(image_upload)

        # 🔍 DEBUG PANEL: Show OCR-extracted text BEFORE analysis
        st.text_area("OCR Extracted Text (Debug)", text, height=200)

        # Warnings for low-quality OCR output
        if (
            text.startswith("[No readable text")
            or text.startswith("[OCR Error")
            or len(text.strip()) == 0
        ):
            warnings.append("OCR could not extract readable text.")

        return {
            "text": text,
            "source_type": "image",
            "warnings": warnings
        }

    # ----------------------------------------------------
    # 4) NO INPUT PROVIDED
    # ----------------------------------------------------
    return {
        "text": "",
        "source_type": None,
        "warnings": ["No input provided."]
    }
