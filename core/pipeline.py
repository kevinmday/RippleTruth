from core.narrative_classifier import analyze_narrative
from core.intention_math import run_intention_math
from core.traceback_engine import run_traceback
from utils.report_templates import build_markdown_report

print("🔍 DEBUG (Cloud): narrative_classifier =", analyze_narrative)
print("🔍 DEBUG (Cloud): intention_math =", run_intention_math)
print("🔍 DEBUG (Cloud): traceback_engine =", run_traceback)


def run_rippletruth_pipeline(text: str) -> dict:
    """
    Main orchestrator for RippleTruth.
    Takes raw text → runs the full pipeline → returns a structured report.
    """

    # -----------------------------------------------------
    # 1. Narrative Analysis (RippleScan Lite)
    # -----------------------------------------------------
    narrative = analyze_narrative(text)

    # -----------------------------------------------------
    # 2. Intention Field Math (FILS, UCIP, TTCF, Drift, RippleScore)
    # -----------------------------------------------------
    intention = run_intention_math(text, narrative)

    # -----------------------------------------------------
    # 3. Traceback / Origin Analysis
    #    FIX: Intention is now passed into traceback.
    # -----------------------------------------------------
    trace = run_traceback(text, narrative, intention)

    # -----------------------------------------------------
    # 4. Build Report (Markdown Output)
    # -----------------------------------------------------
    markdown_report = build_markdown_report(
        narrative=narrative,
        intention=intention,
        traceback=trace
    )

    # -----------------------------------------------------
    # 5. Return everything as a structured object
    # -----------------------------------------------------
    return {
        "markdown": markdown_report,
        "narrative": narrative,
        "intention": intention,
        "traceback": trace
    }

