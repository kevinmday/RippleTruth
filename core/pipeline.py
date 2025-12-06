# ------------------------------------------------------------
# RippleTruth Pipeline — URL + Text + Narrative Engine + FactStack
# ------------------------------------------------------------

# LOCAL IMPORTS
from core.narrative_classifier import analyze_narrative
from core.intention_math import run_intention_math
from core.traceback_engine import run_traceback
from core.interpretation_engine import generate_interpretation
from core.url_engine import fetch_url_text
from core.narrative_engine.narrative_engine import NarrativeEngine
from core.narrative_engine.fact_stack import FactStackEngine      # <-- NEW
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
    # 4. Unified Narrative Engine (PSI-QUANT Integration)
    # ------------------------------------------------------------
    n_engine = NarrativeEngine()
    narrative_engine_output = n_engine.analyze(
        text=text,
        math_results=intention,
        narrative_type=narrative
    )

    # ------------------------------------------------------------
    # 5. FACT-STACK ENGINE (NEW)
    # ------------------------------------------------------------
    fact_engine = FactStackEngine()
    fact_stack_output = fact_engine.analyze(text)

    # ------------------------------------------------------------
    # 6. Interpretation Layer
    #    NOTE: MUST USE POSITIONAL ARGS IN ORDER
    #    Now expects *4* objects:
    #    (narrative, intention, trace, narrative_engine_output)
    # ------------------------------------------------------------
    interpretation = generate_interpretation(
        narrative,
        intention,
        trace,
        narrative_engine_output    # <-- still correct
        # Fact-Stack NOT fed into interpretation yet (v1 design)
    )

    # ------------------------------------------------------------
    # 7. Final Markdown (UI Layer)
    # ------------------------------------------------------------
    markdown_report = build_markdown_report(
        narrative=narrative,
        intention=intention,
        traceback=trace,
        interpretation=interpretation,
        narrative_engine=narrative_engine_output,
        fact_stack=fact_stack_output                # <-- NEW
    )

    # ------------------------------------------------------------
    # 8. Return unified bundle
    # ------------------------------------------------------------
    return {
        "markdown": markdown_report,
        "narrative": narrative,
        "intention": intention,
        "traceback": trace,
        "narrative_engine": narrative_engine_output,
        "fact_stack": fact_stack_output,            # <-- NEW
        "interpretation": interpretation,
        "input_text": text,
        "input_mode": input_mode
    }
