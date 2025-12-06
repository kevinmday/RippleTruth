# =============================================================
# RippleTruth Narrative Engine v2 (Corrected)
# Full-spectrum narrative intelligence orchestrator
# =============================================================

from .narrative_tiers import get_narrative_tier
from .psi_quant import compute_psiquant       # <-- accepts ONLY (text)
from .fact_stack import build_fact_stack
from .world_corpus import score_world_corpus


class NarrativeEngine:
    def __init__(self, use_openai=False, api_key=None):
        self.use_openai = use_openai
        self.api_key = api_key

    # ------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------
    def analyze(self, text, math_results=None, narrative_type=None):
        """
        Performs full-spectrum narrative intelligence:

            1. Tier classification
            2. Fact-Stack extraction
            3. PsiQuant linguistic force estimation
            4. World Corpus alignment heuristic
            5. Optional OpenAI enhancement

        Returns a merged intelligence dictionary compatible with:
            - pipeline.py
            - interpretation_engine.py
            - report_templates.py
        """

        # ---------------------------
        # 1. Determine narrative tier
        # ---------------------------
        tier = get_narrative_tier(text)

        # ---------------------------
        # 2. Build Fact-Stack
        # ---------------------------
        fact_stack = build_fact_stack(text)

        # ---------------------------
        # 3. PsiQuant (linguistic fusion)
        #    IMPORTANT: must not receive extra kwargs
        # ---------------------------
        psiquant = compute_psiquant(text)

        # ---------------------------
        # 4. World Corpus alignment
        # ---------------------------
        corpus_score = score_world_corpus(text)

        # ---------------------------
        # 5. Optional OpenAI enhancement
        # ---------------------------
        openai_summary = None
        if self.use_openai and self.api_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)

                completion = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "Provide a concise forensic narrative analysis."},
                        {"role": "user", "content": text},
                    ]
                )
                openai_summary = completion.choices[0].message["content"]

            except Exception as e:
                openai_summary = f"[OpenAI error: {e}]"

        # ------------------------------------------------------
        # Unified Return Schema (safe for interpretation engine)
        # ------------------------------------------------------
        return {
            "tier": tier,
            "fact_stack": fact_stack,
            "psiquant": psiquant,
            "corpus_alignment": corpus_score,
            "openai_summary": openai_summary,
            "use_openai": self.use_openai
        }
