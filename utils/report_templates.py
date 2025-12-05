import textwrap

# Bind to package so Streamlit Cloud resolves namespace correctly
from rippletruth.core import pipeline


def build_markdown_report(narrative: dict, intention: dict, traceback: dict) -> str:
    """
    Build the full RippleTruth Markdown report.
    This fully matches the working UI layout and uses real intention + traceback fields.
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

    interpretation = trace.get("interpretation", "")
    interpretation_wrapped = textwrap.fill(interpretation, width=90)

    traceback_block = f"""
## 🧭 Traceback / Origin Analysis

**Origin Probability:** {trace.get('origin', 'Unknown')}  
**Amplification Pattern:** {trace.get('amplification', 'Unknown')}  
**Mutation Likelihood:** {trace.get('mutation', 'Unknown')}  

**RippleTruth Index:** {trace.get('rti', 'N/A')}/100

### Interpretation:
{interpretation_wrapped}
"""

    # ------------------------------------------------------------
    # Final Combined Report
    # ------------------------------------------------------------
    full_report = f"""
{narrative_block}

{intention_block}

{traceback_block}

---

### 🧠 RippleTruth Interpretation

This report reflects the combined output of:  
- RippleScan narrative extraction  
- Intention-field analysis  
- Traceback signal inference  

The **RippleTruth Index** integrates polarity, emotional load, origin likelihood,
amplification patterns, and mutation risk into a single reliability score.

---

Generated with **RippleTruth™**  
_Powered by Intention Frameworks_
"""

    return full_report.strip()
