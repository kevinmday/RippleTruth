# ---------------------------------------------------------
# RippleTruth OCR Engine (Fallback Mode)
# ---------------------------------------------------------
# This version is Cloud-safe and removes all heavy OCR deps.
# Image uploads will still be accepted, but OCR will return
# a clear message instead of breaking the app.
# ---------------------------------------------------------

def extract_text_from_image(image_file):
    """
    Fallback OCR handler for Streamlit Cloud.

    Instead of performing real OCR (which requires EasyOCR or
    other heavy dependencies not supported in Cloud), this
    function returns a clean notice so the pipeline can continue
    without failing.
    """

    return (
        "[OCR unavailable on this platform — image processing disabled. "
        "Please use Text or URL mode instead.]"
    )

