# RippleTruth Master Engine
# Wires together: URL loader → cleaner → OCR → classifier → intention math → report builder

from utils.url_loader import load_url
from utils.text_cleaning import clean_text
from utils.report_templates import build_report
from core.ocr_engine import extract_text_from_image
from core.narrative_classifier import classify
from core.intention_math import compute_intention

def process_input(text=None, url=None, image=None):
    """Master entry point for RippleTruth."""

    # 1. Acquire raw text
    if url:
        raw = load_url(url)
    elif image:
        raw = extract_text_from_image(image)
    else:
        raw = text or ""

    # 2. Clean it
    cleaned = clean_text(raw)

    # 3. Classify narrative
    narrative = classify(cleaned)

    # 4. Compute intention math
    intention = compute_intention(cleaned, narrative)

    # 5. Build report object
    report = build_report(
        raw_text=raw,
        cleaned_text=cleaned,
        classification=narrative,
        intention=intention
    )

    return report
