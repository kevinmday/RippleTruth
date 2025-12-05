import easyocr
from PIL import Image
import numpy as np

# Initialize once (Cloud-optimized)
_reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(upload) -> str:
    """
    Cloud-safe OCR using EasyOCR.
    No Tesseract dependency. Works on Streamlit Cloud.
    """

    try:
        # Load image
        image = Image.open(upload).convert("RGB")
        image_np = np.array(image)

        # Run OCR
        results = _reader.readtext(image_np, detail=0)

        if not results:
            return "[No readable text detected in image.]"

        # Join text fragments
        text = "\n".join(results).strip()

        return text if text else "[No readable text detected in image.]"

    except Exception as e:
        return f"[OCR Error: {e}]"
