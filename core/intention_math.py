import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# HELPER: Convert text into TF-IDF vector (semantic anchor)
# ---------------------------------------------------------
def _get_vector(text: str):
    try:
        vect = TfidfVectorizer(stop_words="english")
        X = vect.fit_transform([text])
        return X.toarray()[0]
    except:
        return np.zeros(32)


# ---------------------------------------------------------
# INTENT STRENGTH — measures directive force in language
# ---------------------------------------------------------
def _intent_strength(text: str) -> float:
    strong_words = [
        "must", "will", "never", "always", "ordered",
        "demand", "require", "refuse", "announce",
        "warn", "threaten", "vow", "declare"
    ]

    tokens = text.lower().split()
    if not tokens:
        return 0.0

    score = sum(1 for t in tokens if t in strong_words) / len(tokens)
    return np.clip(score * 4.0, 0, 1)


# ---------------------------------------------------------
# SEMANTIC STABILITY — coherence, low mutation tendency
# ---------------------------------------------------------
def _semantic_stability(text: str) -> float:
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 4]
    if len(sentences) < 2:
        return 0.5

    vectors = [_get_vector(s) for s in sentences]
    sims = []

    for i in range(len(vectors) - 1):
        a = vectors[i].reshape(1, -1)
        b = vectors[i + 1].reshape(1, -1)
        try:
            sims.append(float(cosine_similarity(a, b)))
        except:
            sims.append(0.3)

    avg = np.mean(sims) if sims else 0.3
    return float(np.clip(avg, 0, 1))


# ---------------------------------------------------------
# EMOTIONAL VECTOR — normalized sentiment force
# ---------------------------------------------------------
def _emotional_vector(text: str) -> float:
    positive = ["good", "great", "love", "trust", "hope"]
    negative = ["bad", "terrible", "hate", "fear", "danger"]

    t = text.lower()

    pos = sum(1 for w in positive if w in t)
    neg = sum(1 for w in negative if w in t)

    emo = (pos - neg) / max(1, (pos + neg))
    return float(np.clip((emo + 1) / 2, 0, 1))


# ---------------------------------------------------------
# EMOTIONAL VOLATILITY — amplitude of sentiment swings
# ---------------------------------------------------------
def _emotional_volatility(text: str) -> float:
    tokens = text.lower().split()
    if len(tokens) < 4:
        return 0.1

    emo_values = []
    for t in tokens:
        if t in ["kill", "attack", "threat", "outrage"]:
            emo_values.append(1.0)
        elif t in ["calm", "discuss", "consider"]:
            emo_values.append(0.1)
        else:
            emo_values.append(0.4)

    return float(np.clip(np.std(emo_values), 0, 1))


# ---------------------------------------------------------
# NARRATIVE HARMONICS — multi-frequency intent alignment
# ---------------------------------------------------------
def _narrative_harmonics(text: str) -> float:
    """
    Measures repeating patterns & rhetorical cycles.
    More repetition → stronger harmonic intention field.
    """
    words = text.lower().split()
    if not words:
        return 0.0

    unique = set(words)
    harmonic = (len(words) - len(unique)) / len(words)
    return float(np.clip(harmonic * 3.0, 0, 1))


# ---------------------------------------------------------
# FILS — Future Intention Likelihood Scale
# ---------------------------------------------------------
def compute_fils(intent_strength, stability, emotion):
    return float(np.clip(
        0.6 * intent_strength +
        0.25 * stability +
        0.15 * emotion,
        0, 1
    ))


# ---------------------------------------------------------
# UCIP — Unified Coherence & Intention Probability
# ---------------------------------------------------------
def compute_ucip(fils, stability, harmonics):
    return float(np.clip(
        (0.5 * fils) +
        (0.3 * stability) +
        (0.2 * harmonics),
        0, 1
    ))


# ---------------------------------------------------------
# TTCF — Trump Tensor Chaos Factor (general chaos index)
# ---------------------------------------------------------
def compute_ttcf(volatility, lowband):
    """
    Chaos increases with emotional volatility.
    Low-band signal = longwave drift component.
    """
    return float(np.clip(
        0.7 * volatility +
        0.3 * lowband,
        0, 1
    ))


# ---------------------------------------------------------
# DRIFT — directional change potential
# ---------------------------------------------------------
def compute_drift(fils, ucip, stability_inverse):
    """
    Drift increases when FILS and UCIP diverge
    OR when stability drops.
    """
    drift_raw = abs(fils - ucip) + stability_inverse
    return float(np.clip(drift_raw / 2.0, 0, 1))


# ---------------------------------------------------------
# RIPPLE SCORE — unified intention-field metric
# ---------------------------------------------------------
def compute_ripplescore(fils, ucip, drift):
    """
    Weighted mean of intention + coherence – chaos drift.
    """
    score = (0.45 * fils) + (0.45 * ucip) - (0.25 * drift)
    return float(np.clip(score, 0, 1))


# ---------------------------------------------------------
# MASTER ENGINE — MAIN FUNCTION
# ---------------------------------------------------------
def run_intention_math(text: str, narrative: dict) -> dict:
    """
    The REAL RippleTruth Intention Engine.
    Computes FILS, UCIP, TTCF, Drift, RippleScore using
    Kevin Day’s intention-field equations.
    """

    # ---- Extract raw narrative signals ----
    intent_strength = _intent_strength(text)
    stability = _semantic_stability(text)
    emotion = _emotional_vector(text)
    volatility = _emotional_volatility(text)
    harmonics = _narrative_harmonics(text)

    # ---- Apply intention math ----
    fils = compute_fils(intent_strength, stability, emotion)
    ucip = compute_ucip(fils, stability, harmonics)
    ttcf = compute_ttcf(volatility, volatility * 0.2)
    drift = compute_drift(fils, ucip, (1 - ttcf))
    ripplescore = compute_ripplescore(fils, ucip, drift)

    return {
        "FILS": round(fils, 4),
        "UCIP": round(ucip, 4),
        "TTCF": round(ttcf, 4),
        "Drift": round(drift, 4),
        "RippleScore": round(ripplescore, 4),

        # Debug signals (optional for UI)
        "debug": {
            "intent_strength": intent_strength,
            "stability": stability,
            "emotion": emotion,
            "volatility": volatility,
            "harmonics": harmonics,
        }
    }
