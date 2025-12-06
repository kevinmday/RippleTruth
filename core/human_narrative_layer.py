# ------------------------------------------------------------
# RippleTruth Human Narrative Layer
# ------------------------------------------------------------
# Converts intention-field metrics into a human-readable
# narrative for normal users: Who, What, Where, When, Why.
# ------------------------------------------------------------

def human_narrative_summary(narrative, metrics):
    """
    narrative: dict from RippleScan (topic, polarity, tone, structure)
    metrics: dict from intention_math (FILS, UCIP, TTCF, Drift, RippleScore)
    """

    topic = narrative.get("topic", "Unknown").lower()
    polarity = narrative.get("polarity", "Neutral").lower()
    tone = narrative.get("tone", "Neutral").lower()
    structure = narrative.get("structure", "General Statement").lower()

    fils = metrics.get("FILS", 0)
    ucip = metrics.get("UCIP", 0)
    ttcf = metrics.get("TTCF", 0)
    drift = metrics.get("Drift", 0)
    score = metrics.get("RippleScore", 0)

    # ------------------------------------------------------------
    # WHO (probable source category)
    # ------------------------------------------------------------
    if score < 0.15:
        who = "likely a private individual expressing a low-impact opinion"
    elif score < 0.35:
        who = "consistent with commentary-style messaging or early-stage political framing"
    elif score < 0.65:
        who = "similar to messaging from advocacy groups, political actors, or issue influencers"
    else:
        who = "high-intensity messaging often seen in coordinated political operations or strategic comms"

    # ------------------------------------------------------------
    # WHAT (intent of the message)
    # ------------------------------------------------------------
    if fils < 0.25:
        what = "sets context without pushing a specific conclusion"
    elif fils < 0.5:
        what = "attempts to shape perception or guide interpretation subtly"
    else:
        what = "directs the audience toward a clear emotional or political position"

    # ------------------------------------------------------------
    # WHERE (position within narrative cycle)
    # ------------------------------------------------------------
    if drift < 0.2:
        where = "appears early in the narrative cycle — no momentum yet"
    elif drift < 0.45:
        where = "sits in the middle phase of narrative development"
    else:
        where = "sits in a volatile narrative region where messaging may intensify"

    # ------------------------------------------------------------
    # WHEN (urgency)
    # ------------------------------------------------------------
    if ttcf < 0.15:
        when = "low urgency — stable emotional landscape"
    elif ttcf < 0.35:
        when = "moderate urgency — emotional fluctuation beginning"
    else:
        when = "high urgency — chaos rising or emotional energy building"

    # ------------------------------------------------------------
    # WHY IT MATTERS (impact + risk)
    # ------------------------------------------------------------
    if score < 0.2:
        why = "The message has limited persuasive force but may seed early-stage framing."
    elif score < 0.45:
        why = "The message contributes to topic priming and audience conditioning."
    elif score < 0.7:
        why = (
            "This message participates actively in shaping beliefs and can influence opinion trends."
        )
    else:
        why = (
            "This message carries strong persuasive force and may drive behavioral alignment "
            "or political mobilization."
        )

    # ------------------------------------------------------------
    # Build the final human-readable narrative
    # ------------------------------------------------------------
    return f"""
### 🧭 Narrative Intelligence Summary (Human Mode)

**Who is likely behind it:**  
This message is **{who}**.

**What the message is trying to do:**  
It **{what}**, delivered with a **{tone} emotional tone** and a **{polarity} polarity**.

**Where it sits in the broader conversation:**  
It **{where}**, based on coherence (UCIP {ucip:.2f}) and drift dynamics ({drift:.2f}).

**When messages like this typically appear:**  
This represents **{when}**, indicating how emotionally charged or chaotic the narrative environment is.

**Why this message matters:**  
{why}

### 📝 Bottom Line
This message is a **{structure}** related to **{topic}**, with a RippleScore of **{score:.2f}**,  
indicating its overall influence potential within the narrative field.
"""
