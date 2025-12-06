# ============================================================
# RippleTruth — Fact-Stack Engine (v1.0)
# Extracts factual claims, evaluates consistency, and produces
# a structured summary + stability score.
# ============================================================

import re
from typing import List, Dict


class FactStackEngine:

    # -------------------------------------------------------
    # Main Entry Point
    # -------------------------------------------------------
    def analyze(self, text: str) -> Dict:
        claims = self.extract_claims(text)
        normalized = self.normalize_claims(claims)
        contradictions = self.detect_contradictions(normalized)
        exaggerations = self.detect_exaggeration(normalized)
        stability = self.compute_stability(normalized, contradictions, exaggerations)

        return {
            "claims": normalized,
            "contradictions": contradictions,
            "exaggerations": exaggerations,
            "stability_score": stability
        }

    # -------------------------------------------------------
    # Step 1 — Extract factual claims (simple declaratives)
    # -------------------------------------------------------
    def extract_claims(self, text: str) -> List[str]:
        raw = re.split(r'(?<=[.!?])\s+', text)

        claims = [
            s.strip() for s in raw
            if len(s.split()) >= 5
            and "?" not in s
            and re.search(r"\b(is|are|was|were|has|have|had|will|did|does|said|claims?)\b", s, re.I)
        ]
        return claims

    # -------------------------------------------------------
    # Step 2 — Normalize claims
    # -------------------------------------------------------
    def normalize_claims(self, claims: List[str]) -> List[str]:
        return [c.lower().strip() for c in claims]

    # -------------------------------------------------------
    # Step 3 — Detect contradictions
    # -------------------------------------------------------
    def detect_contradictions(self, claims: List[str]) -> List[str]:
        contradictions = []

        opposite_pairs = [
            ("did not", "did"),
            ("was not", "was"),
            ("were not", "were"),
            ("false", "true"),
            ("never", "always"),
            ("none", "all"),
        ]

        for a in claims:
            for b in claims:
                if a == b:
                    continue
                for neg, pos in opposite_pairs:
                    if neg in a and pos in b:
                        contradictions.append(f"Conflict between: '{a}' AND '{b}'")

        return contradictions

    # -------------------------------------------------------
    # Step 4 — Detect exaggeration signals
    # -------------------------------------------------------
    def detect_exaggeration(self, claims: List[str]) -> List[str]:
        exaggeration_flags = []

        extreme_words = [
            "everyone", "no one", "always", "never",
            "completely", "entirely", "absolutely",
            "proven", "undeniable", "irrefutable"
        ]

        for c in claims:
            if any(w in c for w in extreme_words):
                exaggeration_flags.append(c)

        return exaggeration_flags

    # -------------------------------------------------------
    # Step 5 — Compute stability score (0–100)
    # -------------------------------------------------------
    def compute_stability(self, claims, contradictions, exaggerations) -> float:
        if not claims:
            return 50.0  # neutral fallback

        base = 90

        base -= len(contradictions) * 12
        base -= len(exaggerations) * 5

        return max(0, min(100, base))


# ============================================================
# REQUIRED PIPELINE WRAPPER
# This exposes the pipeline-level entry point the system expects:
#     build_fact_stack(text, narrative, intention)
# ============================================================

def build_fact_stack(text: str, narrative: Dict = None, intention: Dict = None):
    """
    Wrapper so pipeline imports work.
    Internally calls FactStackEngine.analyze() and returns only the list
    of distilled claims + contradictions/exaggerations as a readable stack.
    """

    engine = FactStackEngine()
    result = engine.analyze(text)

    stack = []

    # Claims
    for c in result.get("claims", []):
        stack.append(f"Claim: {c}")

    # Contradictions
    for c in result.get("contradictions", []):
        stack.append(f"Contradiction: {c}")

    # Exaggerations
    for e in result.get("exaggerations", []):
        stack.append(f"Exaggeration: {e}")

    # Stability Score
    stability = result.get("stability_score")
    stack.append(f"Stability Score: {stability}")

    return stack
