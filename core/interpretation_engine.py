# =============================================================
# RippleTruth Interpretation Engine (v2.0 - POSitional Args)
# Integrates:
#   Narrative → Intention Math → Traceback → Psi-Quant
# =============================================================

def generate_interpretation(narrative, intention, traceback, narrative_engine_output=None):
    """
    Supports BOTH:
        - Legacy 3-arg mode (no psi-quant)
        - New 4-arg mode with full narrative-engine intelligence
    """

    # =========================================================
    # Legacy fallback mode (3 arguments)
    # =========================================================
    if narrative_engine_output is None:
        return _generate_legacy_interpretation(narrative, intention, traceback)

    # =========================================================
    # Extract Psi-Quant block
    # =========================================================
    psi = narrative_engine_output.get("psi_quant", {})

    psi_score       = psi.get("psi_score", 0)
    emotionality    = psi.get("emotionality", 0)
    chaos_factor    = psi.get("chaos_factor", 0)
    coherence       = psi.get("coherence", 0)
    intent_strength = psi.get("intent_strength", 0)

    # Human-readable labels
    force_label = (
        "HIGH" if psi_score >= 70 else
        "MODERATE" if psi_score >= 40 else
        "LOW"
    )

    emotionality_note = (
        "strong emotional propulsion"
        if emotionality > 0.35 else
        "moderate emotional coloring"
        if emotionality > 0.15 else
        "minimal emotional coloration"
    )

    chaos_note = (
        "high linguistic volatility"
        if chaos_factor > 0.35 else
        "moderate variability"
        if chaos_factor > 0.15 else
        "stable linguistic structure"
    )

    coherence_note = (
        "high structural coherence"
        if coherence > 0.65 else
        "mixed coherence"
        if coherence > 0.35 else
        "fragmented or uneven structure"
    )

    intent_note = (
        "strong directive pressure"
        if intent_strength > 0.35 else
        "mild directive cues"
        if intent_strength > 0.10 else
        "little directive signaling"
    )

    # =========================================================
    # Reuse your existing interpretation logic
    # =========================================================
    legacy_block = _generate_legacy_interpretation(
        narrative,
        intention,
        traceback
    )

    # =========================================================
    # Build the PSI-QUANT interpretation block
    # =========================================================
    psi_block = (
        f"The text exhibits a **{force_label} narrative influence force**, "
        f"with a Psi-Quant score of **{psi_score}**. "
        f"It demonstrates {emotionality_note}, {chaos_note}, and "
        f"{coherence_note}. Directive intent is characterized by {intent_note}. "
    )

    # =========================================================
    # FUSED OUTPUT — Legacy + Psi-Quant
    # =========================================================
    return {
        "summary": f"Narrative Influence Level: {force_label}",
        "legacy_interpretation": legacy_block,
        "psi_quant_analysis": psi_block,
        "psi_quant_score": psi_score,
        "force_label": force_label,
        "psi_details": {
            "emotionality": emotionality,
            "chaos_factor": chaos_factor,
            "coherence": coherence,
            "intent_strength": intent_strength
        },
        "fused_interpretation_paragraph":
            f"{legacy_block} {psi_block}"
    }


# =============================================================
# INTERNAL: Legacy 3-block interpretation (unchanged)
# =============================================================

def _generate_legacy_interpretation(narrative, intention, traceback):
    """
    Your existing v1 interpreter — preserved exactly.
    """

    topic      = narrative.get("topic")
    polarity   = narrative.get("polarity")
    tone       = narrative.get("tone")
    structure  = narrative.get("structure")

    FILS        = intention.get("FILS")
    UCIP        = intention.get("UCIP")
    TTCF        = intention.get("TTCF")
    Drift       = intention.get("Drift")
    RippleScore = intention.get("RippleScore")

    actor_probs = traceback.get("actor_probabilities", {})
    top_actor   = max(actor_probs, key=actor_probs.get) if actor_probs else "Unknown"
    amp         = traceback.get("amplification_pattern")
    mut         = traceback.get("mutation_likelihood")
    rti         = traceback.get("RippleTruthIndex")

    # Narrative summary
    narrative_summary = (
        f"The text presents a **{topic.lower()}** narrative with a "
        f"**{polarity.lower()} polarity**, delivered in a **{tone.lower()} tone**, "
        f"and structured as a **{structure.lower()}**. "
    )

    # FILS
    if FILS > 0.65:
        fils_desc = "strong emotional propulsion"
    elif FILS > 0.40:
        fils_desc = "moderate emotional activation"
    else:
        fils_desc = "low emotional propulsion"

    # UCIP
    if UCIP > 0.55:
        ucip_desc = "high internal coherence"
    elif UCIP > 0.30:
        ucip_desc = "moderate coherence"
    else:
        ucip_desc = "low coherence"

    # TTCF
    if TTCF > 0.50:
        ttc_desc = "high chaos/distortion"
    elif TTCF > 0.25:
        ttc_desc = "moderate chaos"
    else:
        ttc_desc = "low chaos"

    # Drift
    if Drift > 0.40:
        drift_desc = "large intention drift"
    elif Drift > 0.20:
        drift_desc = "moderate drift"
    else:
        drift_desc = "minimal drift"

    # RippleScore
    if RippleScore > 0.60:
        rs_desc = "a strong RippleScore"
    elif RippleScore > 0.35:
        rs_desc = "a moderate RippleScore"
    else:
        rs_desc = "a weak RippleScore"

    intention_summary = (
        f"Intention-field metrics show {fils_desc}, paired with {ucip_desc}; "
        f"the signal carries {ttc_desc}. Drift analysis shows {drift_desc}, "
        f"ending with {rs_desc}. "
    )

    # Traceback
    if amp > 0.55:
        amp_desc = "high amplification potential"
    elif amp > 0.30:
        amp_desc = "moderate amplification"
    else:
        amp_desc = "low amplification"

    if mut > 0.55:
        mut_desc = "high mutation likelihood"
    elif mut > 0.30:
        mut_desc = "moderate mutation"
    else:
        mut_desc = "low mutation likelihood"

    traceback_summary = (
        f"Traceback modeling points to **{top_actor}** as the most probable origin. "
        f"The message exhibits {amp_desc}, and mutation analysis indicates {mut_desc}. "
        f"The reliability score is **{round(rti, 1)}/100**. "
    )

    return f"{narrative_summary}{intention_summary}{traceback_summary}"
