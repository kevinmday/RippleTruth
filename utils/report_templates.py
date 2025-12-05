import textwrap

"""
RippleTruth — Report Template Builder
-------------------------------------
This module builds the Markdown report used by the Streamlit UI.
It integrates:

• Narrative Scan (RippleScan Lite)
• Intention Math (FILS, UCIP, TTCF, Drift, RippleScore)
• Traceback Engine
• Interpretation Engine (Option B)

Everything returned here is rendered directly in the Streamlit app.
"""


def build_markdown_report(
    narrative: dict,
    intention: dict,
    traceback: dict,
    interpretation: str
) -> str:
    """
    Build the full RippleTruth Markdown report.
    Now supports the Option B Interpretation Engine.
    """

    # ------------------------------------------------------------
    # 1. Narrative Summary
    # ------------------------------------------------------------
    nar = narrative
    narrative_block = f"""
# RippleTruth Report

## RippleTruth Analysis Report

## 🧩 Narrative Summary (RippleScan Lite)

**Topic:** {nar.get('topic', 'Unknown')}  
**Polarity:** {nar.get('polarity', 'Unknown')}  
**Emotional Tone:** {nar.get('emotion_tone', 'Unknown')}  
**Structure:** {nar.get('structure', 'Unknown')}
"""

    # ------------------------------------------------------------
    # 2. Intention Field Metrics
    # ------------------------------------------------------------
    inten = intention
    intention_block = f"""
## 🔮 Intention Field Metrics

| Metric        | Value |
|---------------|-------|
| FILS          | {inten.get("FILS")} |
| UCIP          | {inten.get("UCIP")} |
| TTCF          | {inten.get("TTCF")} |
| Drift         | {inten.get("Drift")} |
| RippleScore   | {inten.get("RippleScore")} |
"""

    # ------------------------------------------------------------
    # 3. Traceback / Origin Analysis
    # ------------------------------------------------------------
    trace = traceback

    # IMPORTANT: Use the REAL KEYS produced by traceback_engine
    origin_label      = trace.get("origin_label", "Unknown")
    amplification_raw = trace.get("amplification_pattern", "Unknown")
    mutation_raw      = trace.get("mutation_likelihood", "Unknown")
    rti               = trace.get("RippleTruthIndex", "N/A")

    traceback_block = f"""
## 🧭 Traceback / Origin Analysis

**Origin Probability (Top Actor):** {origin_label}  
**Amplification Pattern:** {amplification_raw}  
**Mutation Likelihood:** {mutation_raw}  

**RippleTruth Index:** {rti}/100
"""

    # ------------------------------------------------------------
    # 4. Interpretation Block (from Interpretation Engine)
    # ------------------------------------------------------------
    interpretation_wrapped = textwrap.fill(
        interpretation,
        width=90,
        break_long_words=False,
        replace_whitespace=False
    )

    interpretation_block = f"""
## 🧠 RippleTruth Interpretation

{interpretation_wrapped}
"""

    # ------------------------------------------------------------
    # 5. Final Combined Report
    # ------------------------------------------------------------
    full_report = f"""
{narrative_block}

{intention_block}

{traceback_block}

{interpretation_block}

---

### System Notes

This report reflects the combined output of:  
- RippleScan narrative extraction  
- Intention-field analysis  
- Traceback signal inference  
- Interpretation engine (intention × structure × propagation)

The **RippleTruth Index** merges polarity, emotional load, origin likelihood,
amplification patterns, and mutation risk into a single reliability score.

---

Generated with **RippleTruth™**  
_Powered by Intention Frameworks_
"""

    return full_report.strip()
