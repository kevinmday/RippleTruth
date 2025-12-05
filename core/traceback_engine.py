import numpy as np

# Bind to package namespace for Streamlit Cloud resolution
from rippletruth.core import intention_math


# ---------------------------------------------------------
# Actor Probability Templates
# These are NOT classifications — they are priors.
# Traceback adjusts them using intention-field math.
# ---------------------------------------------------------
ACTOR_PRIORS = {
    "Political Actor": 0.32,
    "Media / Journalist": 0.22,
    "Citizen / Civilian": 0.28,
    "Institution / Organization": 0.18,
}


# ---------------------------------------------------------
# Mutation Likelihood — stability inverse + volatility
# ---------------------------------------------------------
def _mutation_likelihood(stability: float, volatility: float) -> float:
    mut = (1 - stability) * 0.6 + volatility * 0.4
    return float(np.clip(mut, 0, 1))


# ---------------------------------------------------------
# Amplification Pattern — coherence vs chaos
# ---------------------------------------------------------
def _amplification_pattern(ucip: float, ttcf: float) -> float:
    """
    Low amplification = stable, low-chaos signals  
    High amplification = chaotic, unstable, emotionally peaked
    """
    amp = (ucip * 0.5) - (ttcf * 0.5)
    return float(np.clip((amp + 1) / 2, 0, 1))


# ---------------------------------------------------------
# Core Actor Scoring Formula
# ---------------------------------------------------------
def _score_actor(intent_strength, stability, harmonics, ripplescore):
    """
    Each actor profile gains/loses probability
    depending on intention-field signature.
    """

    base = np.array(list(ACTOR_PRIORS.values()))

    intent_wt = np.array([1.0, 0.6, 0.4, 0.2])
    stability_wt = np.array([0.9, 1.0, 0.6, 0.8])
    harmonic_wt = np.array([1.0, 1.2, 0.3, 0.8])
    ripple_wt = np.array([1.1, 1.0, 0.5, 0.9])

    scores = (
        base
        * (1 + intent_strength * intent_wt)
        * (1 + stability * stability_wt)
        * (1 + harmonics * harmonic_wt)
        * (1 + ripplescore * ripple_wt)
    )

    probs = scores / scores.sum()
    return {actor: float(probs[i]) for i, actor in enumerate(ACTOR_PRIORS.keys())}


# ---------------------------------------------------------
# Traceback Engine (REAL VERSION)
# ---------------------------------------------------------
def run_traceback(text: str, narrative: dict, intention: dict | None = None) -> dict:
    """
    REAL RippleTruth Traceback Engine.
    Computes:
      - actor probability distribution
      - amplification pattern
      - mutation likelihood
      - RippleTruth Index (0–100)
      - interpretation text
    """

    # -----------------------------------------------------
    # 1) Require REAL intention math
    # -----------------------------------------------------
    if not intention:
        return {
            "actor_probabilities": {},
            "amplification_pattern": 0,
            "mutation_likelihood": 0,
            "RippleTruthIndex": 0,
            "interpretation": "Intention signals missing — traceback skipped.",
        }

    # Pull raw intention signals
    ils = intention["debug"]
    intent_strength = ils["intent_strength"]
    stability = ils["stability"]
    emotion = ils["emotion"]
    volatility = ils["volatility"]
    harmonics = ils["harmonics"]

    fils = intention["FILS"]
    ucip = intention["UCIP"]
    ttcf = intention["TTCF"]
    drift = intention["Drift"]
    ripplescore = intention["RippleScore"]

    # -----------------------------------------------------
    # 2) Actor probability estimation
    # -----------------------------------------------------
    actor_probs = _score_actor(
        intent_strength=intent_strength,
        stability=stability,
        harmonics=harmonics,
        ripplescore=ripplescore,
    )

    # -----------------------------------------------------
    # 3) Mutation likelihood
    # -----------------------------------------------------
    mutation = _mutation_likelihood(stability, volatility)

    # -----------------------------------------------------
    # 4) Amplification behavior (UCIP × TTCF)
    # -----------------------------------------------------
    amplification = _amplification_pattern(ucip, ttcf)

    # -----------------------------------------------------
    # 5) RippleTruth Index
    # -----------------------------------------------------
    rti = (
        (0.35 * stability)
        + (0.25 * ucip)
        + (0.15 * (1 - ttcf))
        + (0.15 * ripplescore)
        + (0.10 * (1 - drift))
    )
    rti = float(np.clip(rti * 100, 1, 99))

    # -----------------------------------------------------
    # 6) Interpretation
    # -----------------------------------------------------
    dominant_actor = max(actor_probs, key=actor_probs.get)

    interpretation = (
        f"A narrative originating from **{dominant_actor}** with "
        f"an amplification profile of **{'Low' if amplification < 0.45 else 'High'} amplification**, "
        f"and a mutation likelihood of **{round(mutation, 2)}**, "
        f"produces a RippleTruth reliability score of **{round(rti, 1)}/100**."
    )

    # -----------------------------------------------------
    # 7) Final Output
    # -----------------------------------------------------
    return {
        "actor_probabilities": actor_probs,
        "amplification_pattern": amplification,
        "mutation_likelihood": mutation,
        "RippleTruthIndex": rti,
        "interpretation": interpretation,
    }
