# ------------------------------------------------------------
# RippleTruth Pipeline — URL + Text Aware Version
# ------------------------------------------------------------

# LOCAL IMPORTS
from core.narrative_classifier import analyze_narrative
from core.intention_math import run_intention_math
from core.traceback_engine import run_traceback
from core.interpretation_engine import generate_interpretation
from core.url_engine import fetch_url_text          # ← NEW
from utils.report_templates import build_markdown_report


def load_input(input_data: str, input_mode: str) -> str:
    """
    Normalizes user input into clean text.
    TEXT → returns raw user text
    URL  → fetches page, extracts full article text
    """
    if input_mode == "URL":
        return fetch_url_text(input_data)

    return input_data  # plain text mode


def run_rippletruth_pipeline(input_data: str, input_mode: str = "TEXT") -> dict:
    """
    Main orchestrator for RippleTruth.

    Accepts:
        input_data → raw text OR URL
        input_mode → "TEXT" or "URL"

    Returns:
        dict including markdown report + all metric blocks
    """

    # ------------------------------------------------------------
    # 0. Resolve final text input (TEXT or URL-ingested)
    # ------------------------------------------------------------
    text = load_input(input_data, input_mode)

    # Safety check
    if not text or len(text.strip()) < 10:
        return {
            "error": "No usable text extracted from input. URL may be invalid or article blocked."
        }

    # ------------------------------------------------------------
    # 1. Narrative Analysis
    # ------------------------------------------------------------
    narrative = analyze_narrative(text)

    # ------------------------------------------------------------
    # 2. Intention Math
    # ------------------------------------------------------------
    intention = run_intention_math(text, narrative)

    # ------------------------------------------------------------
    # 3. Traceback / Origin Modeling
    # ------------------------------------------------------------
    trace = run_traceback(text, narrative, intention)

    # ------------------------------------------------------------
    # 4. Interpretation Layer
    #    NOTE: MUST USE POSITIONAL ARGUMENTS IN ORDER
    # ------------------------------------------------------------
    interpretation = generate_interpretation(narrative, intention, trace)

    # ------------------------------------------------------------
    # 5. Final Markdown (UI Layer)
    # ------------------------------------------------------------
    markdown_report = build_markdown_report(
        narrative=narrative,
        intention=intention,
        traceback=trace,
        interpretation=interpretation
    )

    return {
        "markdown": markdown_report,
        "narrative": narrative,
        "intention": intention,
        "traceback": trace,
        "interpretation": interpretation,
        "input_text": text,
        "input_mode": input_mode
    }
