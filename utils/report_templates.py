# =============================================================
# RippleTruth — Markdown Report Renderer (PsiQuant + FactStack)
# =============================================================
# Matches pipeline signature:
#
# build_markdown_report(
#     narrative,
#     intention,
#     traceback,
#     interpretation,
#     narrative_engine=None,
#     fact_stack=None
# )
# =============================================================

import json


# =============================================================
# Safe Section Formatter  (FIXED)
# =============================================================
def _fmt_section(title: str, body) -> str:
    """Uniform section renderer that safely accepts any type."""

    # Normalize all values to string for markdown
    if isinstance(body, (dict, list)):
        body = "```json\n" + json.dumps(body, indent=2) + "\n```"
    else:
        body = str(body)

    return f"## {title}\n{body.strip()}\n\n"


# =============================================================
# Narrative Block
# =============================================================
def _render_narrative_block(narrative: dict) -> str:
    topic     = narrative.get("topic", "Unknown")
    polarity  = narrative.get("polarity", "Unknown")
    tone      = narrative.get("tone", "Unknown")
    structure = narrative.get("structure", "Unknown")

    return f"""
**Topic:** {topic}  
**Polarity:** {polarity}  
**Tone:** {tone}  
**Structure:** {structure}
    """


# =============================================================
# Intention Math Block
# =============================================================
def _render_intention_block(intention: dict) -> str:
    FILS  = intention.get("FILS")
    UCIP  = intention.get("UCIP")
    TTCF  = intention.get("TTCF")
    Drift = intention.get("Drift")
    RS    = intention.get("RippleScore")
    PSI   = intention.get("PsiQuant")

    block = f"""
**FILS (Forward Intention Load):** {FILS}  
**UCIP (Coherence Index):** {UCIP}  
**TTCF (Chaos Factor):** {TTCF}  
**Drift:** {Drift}  
**RippleScore:** {RS}  
"""

    if PSI is not None:
        block += f"**PsiQuant Score:** {PSI}\n"

    return block


# =============================================================
# Traceback Block
# =============================================================
def _render_traceback_block(trace: dict) -> str:
    actors = trace.get("actor_probabilities", {})
    amp    = trace.get("amplification_pattern", 0)
    mut    = trace.get("mutation_likelihood", 0)
    rti    = trace.get("RippleTruthIndex", 0)

    if actors:
        actors_md = "\n".join([f"- **{k}:** {round(v*100,1)}%" for k, v in actors.items()])
    else:
        actors_md = "_No actor data available_"

    return f"""
### Actor Probability Model
{actors_md}

**Amplification Pattern:** {amp}  
**Mutation Likelihood:** {mut}  
**RippleTruth Index:** {round(rti,1)}/100
    """


# =============================================================
# FactStack Block
# =============================================================
def _render_fact_stack_block(fact_stack: dict | None) -> str:
    if not fact_stack:
        return "_No Fact-Stack analysis performed._"

    facts = fact_stack.get("facts", [])
    reliability = fact_stack.get("reliability_score")
    density = fact_stack.get("fact_density")

    out = ""

    if facts:
        out += "**Extracted Facts:**\n"
        for f in facts:
            out += f"- {f}\n"
        out += "\n"
    else:
        out += "_No extractable factual anchors detected._\n\n"

    out += f"**Fact Density:** {density}\n"
    out += f"**Reliability Score:** {reliability}\n"

    return out


# =============================================================
# Narrative Engine Block (PSI-QUANT FUSION)
# =============================================================
def _render_narrative_engine_block(ne: dict | None) -> str:
    if not ne:
        return "_Narrative engine not invoked._"

    tier = ne.get("tier")
    analysis = ne.get("analysis")
    use_openai = ne.get("use_openai")

    return f"""
**Tier:** {tier}  
**Analysis:** {analysis}  
**OpenAI Enabled:** {use_openai}
    """


# =============================================================
# MASTER BUILDER
# =============================================================
def build_markdown_report(
    narrative,
    intention,
    traceback,
    interpretation,
    narrative_engine=None,
    fact_stack=None,
):
    """Builds the full markdown report for UI rendering."""

    report = ""

    # Narrative Layer
    report += _fmt_section("Narrative Analysis", _render_narrative_block(narrative))

    # Intention Math Layer
    report += _fmt_section("Intention Metrics", _render_intention_block(intention))

    # PsiQuant Layer
    if intention.get("PsiQuant") is not None:
        report += _fmt_section("PsiQuant Scoring", f"**PsiQuant:** {intention.get('PsiQuant')}")

    # FactStack Layer
    report += _fmt_section("Fact Stack", _render_fact_stack_block(fact_stack))

    # Narrative Engine Fusion Layer
    report += _fmt_section("Narrative Engine (Fusion)", _render_narrative_engine_block(narrative_engine))

    # Traceback Layer
    report += _fmt_section("Traceback Modeling", _render_traceback_block(traceback))

    # Interpretation Layer
    report += _fmt_section("Interpretation", interpretation)

    return report
