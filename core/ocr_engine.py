from PIL import Image
import pytesseract
import io

def extract_text_from_image(upload) -> str:
    """
    Extracts text from uploaded images using Tesseract OCR.
    Falls back gracefully if OCR fails.
    """

    try:
        # Load image from Streamlit upload object
        image = Image.open(upload)

        # Run OCR
        text = pytesseract.image_to_string(image)

        # Clean up whitespace
        text = text.strip()

        if not text:
            return "[No readable text detected in image.]"

        return text

    except Exception as e:
        return f"[OCR Error: {e}]"
