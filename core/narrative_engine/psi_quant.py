"""
Psi-Quant Narrative Influence Engine
------------------------------------
This module evaluates the *force* of a narrative using a multidimensional scoring
system similar in spirit to MarketMind’s fusion logic.

The goal is not sentiment analysis — it is *intention detection*:
    - influence pressure
    - emotional load
    - destabilization patterns
    - persuasion force
    - chaos signature
    - narrative coherence
    - intention-weighted meaning

Outputs:
    psi_score      → 0–100 overall force
    force_vector   → component weights
    chaos_factor   → similar to TTCF but linguistic
    coherence      → structured vs. disordered messaging
    emotionality   → emotional load index
    modality_shift → level of certainty/assertion vs ambiguity
"""

import re
import statistics


class PsiQuant:
    def __init__(self):
        # Weight configuration — can be tuned later
        self.weights = {
            "emotionality": 0.22,
            "assertion": 0.20,
            "volatility": 0.18,
            "intent_strength": 0.20,
            "coherence": 0.20
        }

    # ---------------------------------------------------------
    # Utility: tokenize and basic cleanup
    # ---------------------------------------------------------
    def _tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    # ---------------------------------------------------------
    # Emotional Load Detection
    # ---------------------------------------------------------
    def _emotionality(self, text):
        emotional_words = [
            "outrage", "corrupt", "evil", "lie", "destroy",
            "fraud", "attack", "stolen", "hate", "traitor",
            "fight", "chaos", "collapse", "disaster"
        ]

        tokens = self._tokenize(text)
        count = sum(1 for t in tokens if t in emotional_words)

        # Normalize by text length
        return min(1.0, count / max(1, len(tokens) / 20))

    # ---------------------------------------------------------
    # Assertion / Modality: measures *certainty*
    # ---------------------------------------------------------
    def _assertion_level(self, text):
        strong_modals = ["will", "must", "cannot", "always", "never"]
        weak_modals = ["might", "could", "possibly", "perhaps"]

        tokens = self._tokenize(text)

        strong = sum(1 for t in tokens if t in strong_modals)
        weak = sum(1 for t in tokens if t in weak_modals)

        score = strong - (weak * 0.5)

        # squash into 0–1
        return max(0, min(1, (score + 3) / 6))

    # ---------------------------------------------------------
    # Volatility / Chaos Signature (linguistic TTCF)
    # ---------------------------------------------------------
    def _linguistic_chaos(self, text):
        fragments = re.split(r"[.!?]", text)
        lengths = [len(f.strip().split()) for f in fragments if f.strip()]

        if len(lengths) < 2:
            return 0.1

        try:
            stdev = statistics.stdev(lengths)
            chaos = stdev / max(1, statistics.mean(lengths))
        except statistics.StatisticsError:
            return 0.1

        return max(0.0, min(1.0, chaos))

    # ---------------------------------------------------------
    # Intent Strength (Directional force)
    # ---------------------------------------------------------
    def _intent_strength(self, text):
        directional_terms = [
            "should", "must", "need to", "urge", "call for",
            "demand", "insist", "push", "drive", "force"
        ]

        count = 0
        for term in directional_terms:
            count += text.lower().count(term)

        # Normalize
        return min(1.0, count / 5)

    # ---------------------------------------------------------
    # Coherence (semantic orderliness vs scatter)
    # ---------------------------------------------------------
    def _coherence(self, text):
        sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

        if len(sentences) < 2:
            return 0.5  # neutral default

        lengths = [len(s.split()) for s in sentences]

        if not lengths:
            return 0.5

        try:
            variance = statistics.variance(lengths)
        except statistics.StatisticsError:
            variance = 0

        # High variance ⇒ lower coherence
        coherence = 1 / (1 + variance ** 0.5)

        return max(0.0, min(1.0, coherence))

    # ---------------------------------------------------------
    # Main compute method
    # ---------------------------------------------------------
    def compute(self, text):
        emotionality = self._emotionality(text)
        assertion = self._assertion_level(text)
        volatility = self._linguistic_chaos(text)
        intent_strength = self._intent_strength(text)
        coherence = self._coherence(text)

        # Weighted fusion
        psi_score = (
            emotionality * self.weights["emotionality"] +
            assertion * self.weights["assertion"] +
            volatility * self.weights["volatility"] +
            intent_strength * self.weights["intent_strength"] +
            coherence * self.weights["coherence"]
        ) * 100

        force_vector = {
            "emotionality": emotionality,
            "assertion_level": assertion,
            "volatility": volatility,
            "intent_strength": intent_strength,
            "coherence": coherence
        }

        return {
            "psi_score": round(psi_score, 2),
            "force_vector": force_vector,
            "chaos_factor": volatility,
            "emotionality": emotionality,
            "assertion": assertion,
            "intent_strength": intent_strength,
            "coherence": coherence
        }


# ================================================================
# Pipeline Compatibility Wrapper
# The pipeline expects: compute_psiquant(text, math_results, narrative)
# ================================================================
def compute_psiquant(text: str, math_results: dict = None, narrative: dict = None):
    """
    Compatibility wrapper — creates a PsiQuant engine instance 
    and returns ONLY the psi_score, because the pipeline expects a scalar.
    """
    engine = PsiQuant()
    result = engine.compute(text)
    return result.get("psi_score", 0)
