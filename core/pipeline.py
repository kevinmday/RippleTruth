# -----------------------------------------
# LOCAL IMPORTS — FIXED
# -----------------------------------------
from core.narrative_classifier import analyze_narrative
from core.intention_math import run_intention_math
from core.traceback_engine import run_traceback
from core.interpretation_engine import generate_interpretation
from utils.report_templates import build_markdown_report


def run_rippletruth_pipeline(text: str) -> dict:
    """
    Main orchestrator for RippleTruth.
    Takes raw text → runs full pipeline → returns structured results.
    """

    # 1. Narrative Analysis
    narrative = analyze_narrative(text)

    # 2. Intention Math
    intention = run_intention_math(text, narrative)

    # 3. Traceback / Origin Analysis
    trace = run_traceback(text, narrative, intention)

    # 4. Interpretation Block (positional args only!)
    interpretation = generate_interpretation(narrative, intention, trace)

    # 5. Final Markdown Report for UI
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
        "interpretation": interpretation
    }
