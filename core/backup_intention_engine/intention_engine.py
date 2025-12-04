import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def normalize(value, min_val=0.0, max_val=1.0):
    """Normalizes a single number to the 0–1 scale."""
    return (value - min_val) / (max_val - min_val) if max_val > min_val else 0.0


def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


# ---------------------------------------------------------
# FILS — Future Intention Likelihood Scale
# ---------------------------------------------------------

def compute_fils(intent_strength, narrative_stability, emotional_vector):
    """
    FILS = 0.6*IntentStrength + 0.25*NarrativeStability + 0.15*EmotionalVector
    All inputs assumed to already be normalized (0–1).
    """

    fils = (
        0.6 * intent_strength +
        0.25 * narrative_stability +
        0.15 * emotional_vector
    )

    return clamp(fils)


# ---------------------------------------------------------
# UCIP — Unified Cosmic Intention Postulate Force
# ---------------------------------------------------------

def compute_ucip(fils, semantic_coherence, narrative_harmonics, entropy):
    """
    UCIP = (FILS * SemanticCoherence * NarrativeHarmonics) / (1 + Entropy)
    """

    denom = 1 + max(entropy, 0.0001)
    ucip = (fils * semantic_coherence * narrative_harmonics) / denom

    return clamp(ucip)


# ---------------------------------------------------------
# TTCF — Trump Tensor Chaos Factor
# ---------------------------------------------------------

def compute_ttcf(emotional_volatility, contradiction_density):
    """
    TTCF = EmotionalVolatility * ContradictionDensity
    """

    ttcf = emotional_volatility * contradiction_density
    return clamp(ttcf)


# ---------------------------------------------------------
# Drift — Magnetic Field Drift Score
# ---------------------------------------------------------

def compute_drift(delta_fils, delta_ucip, ttcf):
    """
    Drift = ΔFILS × ΔUCIP × (1 - TTCF)
    """

    drift = delta_fils * delta_ucip * (1 - ttcf)
    return clamp(drift)


# ---------------------------------------------------------
# RippleScore — Unified Intention Index
# ---------------------------------------------------------

def compute_ripplescore(fils, ucip, ttcf, drift):
    """
    RippleScore = 0.4*FILS + 0.35*UCIP + 0.15*(1 - TTCF) + 0.10*DriftNorm
    """

    drift_norm = clamp(drift)  # Already normalized by definition

    score = (
        0.4 * fils +
        0.35 * ucip +
        0.15 * (1 - ttcf) +
        0.10 * drift_norm
    )

    return clamp(score)
