def safe_get(dictionary: dict, key: str, default=None):
    """
    Safely fetches a key from a dictionary.
    """
    try:
        return dictionary.get(key, default)
    except Exception:
        return default


def truncate(text: str, max_len: int = 300):
    """
    Shortens long text for previews without breaking the UI.
    """
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."
