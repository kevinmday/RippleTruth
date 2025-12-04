import re
import textwrap

def analyze_narrative(text: str) -> dict:
    """
    RippleScan Lite: Performs basic topic detection, polarity,
    emotional tone, and structure extraction.
    """

    cleaned = text.lower().strip()

    # ---------------------------
    # Topic Detection (Very Simple)
    # ---------------------------
    topic = detect_topic(cleaned)

    # ---------------------------
    # Sentiment / Polarity
    # ---------------------------
    polarity = detect_polarity(cleaned)

    # ---------------------------
    # Emotional Tone (Simple Keyword-Based)
    # ---------------------------
    tone = detect_emotional_tone(cleaned)

    # ---------------------------
    # Narrative Structure
    # ---------------------------
    structure = detect_structure(cleaned)

    return {
        "topic": topic,
        "polarity": polarity,
        "tone": tone,
        "structure": structure
    }


# ==========================================================
# TOPIC DETECTION
# ==========================================================
def detect_topic(text: str) -> str:
    if any(k in text for k in ["immigration", "border", "migrant"]):
        return "Immigration"

    if any(k in text for k in ["economy", "inflation", "jobs", "market"]):
        return "Economy"

    if any(k in text for k in ["election", "vote", "campaign", "ballot"]):
        return "Elections"

    if any(k in text for k in ["crime", "violence", "police"]):
        return "Crime"

    if any(k in text for k in ["war", "military", "strike", "attack"]):
        return "Foreign Policy"

    return "General"


# ==========================================================
# POLARITY DETECTION
# ==========================================================
def detect_polarity(text: str) -> str:
    positive_words = ["good", "hope", "success", "progress", "peace"]
    negative_words = ["bad", "fear", "danger", "threat", "corrupt", "fraud"]

    pos = sum(1 for w in positive_words if w in text)
    neg = sum(1 for w in negative_words if w in text)

    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"


# ==========================================================
# EMOTIONAL TONE
# ==========================================================
def detect_emotional_tone(text: str) -> str:
    if any(k in text for k in ["panic", "fear", "urgent", "chaos", "anger"]):
        return "High Emotional Load"

    if any(k in text for k in ["concern", "worry", "uncertain"]):
        return "Moderate Emotional Load"

    return "Low Emotional Load"


# ==========================================================
# STRUCTURE DETECTION
# ==========================================================
def detect_structure(text: str) -> str:
    """
    Simple heuristic:
    - Look for claims, assertions, evidence patterns.
    """

    if "because" in text or "due to" in text:
        return "Claim with Reason"

    if "therefore" in text or "thus" in text:
        return "Argument / Conclusion"

    if "report" in text or "sources say" in text:
        return "Reported Information"

    if "!" in text:
        return "Emphatic / Emotional Statement"

    return "General Statement"
