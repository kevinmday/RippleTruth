# =============================================================
# RippleTruth Interpretation Engine (v1.0 - POSitional Args Only)
# Produces a deep, human-readable forensic explanation
# integrating Narrative → Intention Math → Traceback.
# =============================================================

def generate_interpretation(narrative, intention, traceback):
    """
    POS-ONLY version used by the current pipeline.

    Args:
        narrative (dict)
        intention (dict)
        traceback (dict)

    Returns:
        str - A unified interpretation paragraph.
    """

    # ---------------------------------
    # Narrative extraction
    # ---------------------------------
    topic      = narrative.get("topic")
    polarity   = narrative.get("polarity")
    tone       = narrative.get("tone")
    structure  = narrative.get("structure")

    # ---------------------------------
    # Intention math extraction
    # ---------------------------------
    FILS        = intention.get("FILS")
    UCIP        = intention.get("UCIP")
    TTCF        = intention.get("TTCF")
    Drift       = intention.get("Drift")
    RippleScore = intention.get("RippleScore")

    # ---------------------------------
    # Traceback extraction
    # ---------------------------------
    actor_probs = traceback.get("actor_probabilities", {})
    top_actor   = max(actor_probs, key=actor_probs.get) if actor_probs else "Unknown"
    amp         = traceback.get("amplification_pattern")
    mut         = traceback.get("mutation_likelihood")
    rti         = traceback.get("RippleTruthIndex")

    # ---------------------------------
    # Narrative summary
    # ---------------------------------
    narrative_summary = (
        f"The text presents a **{topic.lower()}** narrative with a "
        f"**{polarity.lower()} polarity**, delivered in a **{tone.lower()} tone**, "
        f"and structured as a **{structure.lower()}**. "
    )

    # ---------------------------------
    # FILS interpretation
    # ---------------------------------
    if FILS > 0.65:
        fils_desc = "strong emotional propulsion driving reader direction"
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

    # ---------------------------------
    # Traceback interpretation
    # ---------------------------------
    if amp > 0.55:
        amp_desc = "high amplification potential"
    elif amp > 0.30:
        amp_desc = "moderate amplification"
    else:
        amp_desc = "low amplification"

    if mut > 0.55:
        mut_desc = "high mutation likelihood"
    elif mut > 0.30:
        mut_desc = "moderate mutation likelihood"
    else:
        mut_desc = "low mutation likelihood"

    traceback_summary = (
        f"Traceback modeling points to **{top_actor}** as the most probable origin. "
        f"The message exhibits {amp_desc}, and mutation analysis indicates {mut_desc}. "
        f"The reliability score is **{round(rti,1)}/100**. "
    )

    # ---------------------------------
    # Final block
    # ---------------------------------
    final_block = (
        f"{narrative_summary}{intention_summary}{traceback_summary}"
    )

    return final_block
