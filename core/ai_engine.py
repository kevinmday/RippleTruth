# core/ai_engine.py

import openai

"""
AI Enhancement Engine for RippleTruth
-------------------------------------
This module provides optional, user-supplied AI capabilities
for richer narrative intelligence summaries, counter-narratives,
and extended analysis.

The app NEVER stores API keys — they remain only in Streamlit session_state.
"""


def run_ai_enhancement(text: str, api_key: str, mode: str = "summary") -> str:
    """
    Enhance a narrative using OpenAI models.

    modes:
        - summary:  Human-style intelligence brief
        - counter:  Counter-narrative to neutralize influence
        - expand:   Multi-paragraph analytical expansion
        - brief:    3–5 sentence executive summary

    Returns:
        str: enhanced text output from the model
    """

    if not api_key:
        return "⚠️ No API key provided — AI enhancements disabled."

    openai.api_key = api_key

    # Prompt library — extendable later
    prompts = {
        "summary": (
            "You are a senior narrative intelligence analyst. Write a clear, "
            "concise, human-readable intelligence summary of the following message. "
            "Explain the narrative function, likely intent, audience impact, and "
            "why the message matters.\n\n"
            f"Message:\n{text}"
        ),
        "counter": (
            "You are an expert in counter-messaging. Write a factual, non-emotional "
            "counter-narrative that neutralizes manipulative or misleading implications "
            "in the following message. Do not mock or attack the author — just provide clarity.\n\n"
            f"Message:\n{text}"
        ),
        "expand": (
            "Expand the following message into a 3–4 paragraph intelligence brief. "
            "Cover narrative structure, psychological framing, intent signals, emotional "
            "load, influence pathways, and overall risk profile.\n\n"
            f"Message:\n{text}"
        ),
        "brief": (
            "Condense the following into a tight 4–5 sentence executive summary suitable "
            "for a security or intelligence decision-maker.\n\n"
            f"Message:\n{text}"
        ),
    }

    prompt = prompts.get(mode, prompts["summary"])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional analyst specializing in narrative dynamics, "
                        "information influence, and intention mapping. "
                        "Write clearly, factually, and without bias."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.4,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ AI enhancement failed: {e}"
