import re

def clean_text(text: str) -> str:
    """
    Basic text normalization:
    - Lowercase
    - Remove excessive whitespace
    - Strip control characters
    """

    if not text:
        return ""

    # Lowercase normalization
    cleaned = text.lower()

    # Remove control characters
    cleaned = re.sub(r"[\r\n\t]+", " ", cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
